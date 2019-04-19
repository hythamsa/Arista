
#!/usr/local/bin/python3

import requests, json, csv, argparse, sys
from pprint import pprint


def main():
	# Disable SSL self-signed cert warnings
	requests.packages.urllib3.disable_warnings()

	# Define command line flags
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', dest='user', required='True', help='Username for switch auth')
	parser.add_argument('-p', '--passwd', dest='passwd', required='True', help='Password for switch auth')
	parser.add_argument('-s', '--server', dest='server', required='True', help='IP adddress or hostname of the CVP server')
	args = parser.parse_args()

	# If no argument is supplied, print help
	if len(sys.argv[1:]) == 0:
		parser.print_help()
		parser.exit()

	user = args.user
	passwd = args.passwd
	server = args.server


	baseuri = "https://{}/cvpservice".format(server)

	auth_data = json.dumps({'userId': user, 'password': passwd})
	auth_url = (baseuri + "/login/authenticate.do")
	auth_resp = requests.post(auth_url,data=auth_data,verify=False)
	cookies = auth_resp.cookies

	
	inventory = (baseuri + "/inventory/devices")
	get_inventory = requests.get(inventory, cookies=cookies, verify=False)
	get_inventory_json = get_inventory.json()
	pprint(get_inventory_json)

if __name__ == '__main__':
	main()