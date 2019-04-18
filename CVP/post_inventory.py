import requests, json, csv, argparse, sys

'''
Python 3.x

Requires:
Python3

Module requirements:
requests
json
argparse

To install modules:
pip3 install requests
pip3 install json
pip3 install argparse

Quick Description:
Bulk upload switches into CVP assigned to "undefined" container (for now). No CSV input (again... for now), and switch definition is only done via "-s" flag for the time being

Required flags:
-u (username)
-p (password)
-sr (CVP Server Name/IP)
-s (list of switches separated by a comma) This is only a requirement until CSV infile is coded

Usage:
python3 test-code.py -u cvpadmin -p cvpadmin --server cvp -s 10.92.62.47,10.92.62.48,10.92.61.208,10.92.61.207,10.92.61.206,10.92.61.210,10.92.61.205

'''
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