import ssl, csv, argparse, sys, getpass
from jsonrpclib import Server

class color:
    HEADER = '\033[95m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Non-verfication of self-signed certificate - BAD
ssl._create_default_https_context = ssl._create_unverified_context


def Arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', dest='user', help='Username for switch auth')
    parser.add_argument('-p', '--password', dest='passwd', help='Password for switch auth')
    parser.add_argument('-m', '--method', dest='method', default='https', help='Select protocol', choices=['http', 'https'])
    parser.add_argument('-e', '--enable', dest='enable', help='Enable password if configured')
    parser.add_argument('-c', '--csvinfile', dest='csvinfile', help='Provide the name of the CSV input file.')
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
    	parser.print_help()
    	parser.exit()

    return verifyargs(args)


def verifyargs(args):
	if args.user is None:
		args.user = str(raw_input("What is the switch username? "))

	if args.passwd is None:
		args.passwd = getpass.getpass()

	if args.csvinfile is None:
		args.csvinfile = str(raw_input("What is the name of the CVS input file? "))

	return args


def provisionVxlan(user,passwd,method,csvinfile):
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
				config_vxlan = cmdapi.runCmds(1,["enable", "configure", "interface vxlan1", "vxlan vlan add " + vlid + " vni " + vxlan])
				config_svi = cmdapi.runCmds(1,["enable", "configure", "interface vlan " + vlid, "description " + descr, "vrf forwarding " + vrf, "ip address virtual " + ipaddress ])
				# Retrieve BGP ASN & Router ID
				shipbgp = cmdapi.runCmds(1,["show ip bgp summary"])
				asn = shipbgp[0]['vrfs']['default']['asn']
				rtrid = shipbgp[0]['vrfs']['default']['routerId']
				config_rd = cmdapi.runCmds(1,["enable", "configure", "router bgp " + str(asn), "vlan " + vlid, "rd " + rtrid+":"+vxlan, "route-target both " + vlid+":"+vxlan, "redistribute learned"])


def main():
	options = Arguments()
	provisionVxlan(options.user,options.passwd,options.method,options.csvinfile)


if __name__ == '__main__':
	main()