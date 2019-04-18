import requests, json, csv, argparse, sys


def main():
	# Define command line flags
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', dest='user', required='True', help='Username for switch auth')
	parser.add_argument('-p', '--passwd', dest='passwd', required='True', help='Password for switch auth')
	parser.add_argument('-s', '--switch', dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
	parser.add_argument('-c', '--csvinfile', dest='csvinfile', help='CSV Input File')
	parser.add_argument('-sr', '--server', dest='server', required='True', help='IP adddress or hostname of the CVP server')
	args = parser.parse_args()

	# If no argument is supplied, print help
	if len(sys.argv[1:]) == 0:
		parser.print_help()
		parser.exit()

	user = args.user
	passwd = args.passwd
	csvinfile = args.csvinfile
	switch_list = args.switch
	if not switch_list == None:
		switch = switch_list.split(",")
	server = args.server


	hosts = json.dumps({'hosts': switch})
	baseuri = "https://{}/cvpservice".format(server)

	auth_data = json.dumps({'userId': user, 'password': passwd})
	auth_url = (baseuri + "/login/authenticate.do")
	auth_resp = requests.post(auth_url,data=auth_data,verify=False)
	cookies = auth_resp.cookies

	
	inventory = (baseuri + "/inventory/devices")
	post_inventory = requests.post(inventory,cookies=cookies,data=hosts,verify=False)
	print(post_inventory.status_code)
	print(post_inventory.content)
	

if __name__ == '__main__':
	main()