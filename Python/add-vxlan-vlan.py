#!/usr/bin/python

'''
Add new VXLAN enabled VLANs, along with associated SVIs assigned to existing VRFs. Please note that this script will NOT create a new VRF

Example use:
python add-vxlan-vlan.py -u admin -p admin -m http -c vxlan-vlan_INPUT.csv
'''

import ssl, csv, datetime, argparse, sys
from jsonrpclib import Server

# Non-verfication of self-signed certificate - BAD
ssl._create_default_https_context = ssl._create_unverified_context
today = datetime.date.today()

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', dest='user', help='Username for switch auth')
parser.add_argument('-p', '--password', dest='passwd', help='Password for switch auth')
parser.add_argument('-m', '--method', dest='method', help='Select protocol', choices=['http', 'https'])
parser.add_argument('-e', '--enable', dest='enable', help='Enable password if configured')
parser.add_argument('-c', '--csvinfile', dest='csvinfile', help='Provide the name of the CSV input file.')
args = parser.parse_args()

# If not argument is supplied, print help
if len(sys.argv[1:]) ==	0:
	parser.print_help()
	parser.exit()

user = args.user
passwd = args.passwd
method = args.method
enable = args.enable
csvinfile = args.csvinfile

with open (csvinfile, 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		host = row['switch']
		vlid = row['vlan-id']
		vname = row['vlan_name']
		ipaddress = row['ip_address']
		vrf = row['vrf']
		descr = row['description']

		for a in host:
		# Create VXLAN adding VLAN ID to 20000
			vxlan = str(int(vlid) + 20000)
			cmdapi = Server("%s://%s:%s@%s/command-api" % (method,user,passwd,host))
			config_vlan = cmdapi.runCmds(1,["enable", "configure", "vlan " + vlid, "name " + vname])
			config_vxlan = cmdapi.runCmds(1,["enable", "configure", "interface vxlan1", "vxlan vlan " + vlid + " vni " + vxlan])
			config_svi = cmdapi.runCmds(1,["enable", "configure", "interface vlan " + vlid, "description " + descr, "vrf forwarding " + vrf, "ip address virtual " + ipaddress ])
			# Retrieve BGP ASN & Router ID
			shipbgp = cmdapi.runCmds(1,["show ip bgp summary"])
			asn = shipbgp[0]['vrfs']['default']['asn']
			rtrid = shipbgp[0]['vrfs']['default']['routerId']
			config_rd = cmdapi.runCmds(1,["enable", "configure", "router bgp " + str(asn), "vlan " + vlid, "rd " + rtrid+":"+vxlan, "route-target both " + vlid+":"+vxlan, "redistribute learned"])