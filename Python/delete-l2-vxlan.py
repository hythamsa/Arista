#!/usr/bin/python

import ssl, csv, argparse, sys
from jsonrpclib import Server

# Non-verfication of self-signed certificate - BAD
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', dest='user', help='Username for switch auth')
parser.add_argument('-p', '--passwd', dest='passwd', help='Password for switch auth')
parser.add_argument('-m', '--method', dest='method', help='Select protocol', choices=['http', 'https'])
parser.add_argument('-e', '--enable', dest='enable', help='Enable password if configured')
parser.add_argument('-c', '--csvinfile', dest='csvinfile', help='Provide the name of the CSV input file')
args = parser.parse_args()

if len(sys.argv[1:]) == 0:
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
		vname = row['vlname']

		#use vlan ID as VNI
		cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,host))
		config_vlan = cmdapi.runCmds(1,["enable", "configure", "no vlan " + vlid])
		config_vxlan = cmdapi.runCmds(1,["enable", "configure", "interface vxlan1", "no vxlan vlan " + vlid + " vni " + vlid])

		#Retrieve BGP ASN and Router ID for RD and RT assignment
		shipbgp = cmdapi.runCmds(1,["show ip bgp summary"])
		asn = shipbgp[0]['vrfs']['default']['asn']
		rtrid = shipbgp[0]['vrfs']['default']['routerId']
		config_rdrt = cmdapi.runCmds(1,["enable", "configure", "router bgp " + str(asn), "no vlan " + vlid])