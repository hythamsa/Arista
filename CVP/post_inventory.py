import requests, json, csv, argparse, sys


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

def readme():
	print(color.HEADER + color.BOLD + 'Python 3.x' + color.END)
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Requires:' + color.END)
	print('Python 3')
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Module requirements:' + color.END)
	print('requests')
	print('json')
	print('argparse')
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'To install modules:' + color.END)
	print('pip3 install requests')
	print('pip3 install json')
	print('pip3 install argparse')
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Quick Description:' + color.END)
	print('Bulk upload switches into CVP assigned to "undefined" container (for now) using input directly from the command line using the "-s" switch OR using a CSV Input file leveraging "-c"')
	print(color.BOLD + 'Please NOTE that you cannot use both "-s" or "-c" at the same time. See usage below' + color.END)
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Required Flags:' + color.END)
	print('-u <username>')
	print('-p <password>')
	print('-sr <CVP FQDN or IP>')
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Optional Flags:' + color.END)
	print('-s <switch names or IP addresses separated by a comma (,)>')
	print('-c <CSV file name>')
	print('')
	print(color.RED + color.BOLD + color.UNDERLINE + 'Usage:' + color.END)
	print('python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -s 10.92.62.47,10.92.62.48,10.92.61.208,10.92.61.207,10.92.61.206,10.92.61.210,10.92.61.205')
	print('python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -c inventory.csv')


def main():
	global csvinfile,user,passwd,server,cookies,baseuri,switch
	requests.packages.urllib3.disable_warnings()

	# Define command line flags
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', dest='user', help='Username for switch auth')
	parser.add_argument('-p', '--passwd', dest='passwd', help='Password for switch auth')
	parser.add_argument('-s', '--switch', dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
	parser.add_argument('-c', '--csvinfile', dest='csvinfile', help='CSV Input File')
	parser.add_argument('-sr', '--server', dest='server', help='IP adddress or hostname of the CVP server')
	args = parser.parse_args()

	# If no argument is supplied, print help
	if len(sys.argv[1:]) == 0:
		parser.print_help()
		print(color.BOLD + '#' * 180 + color.END)
		readme()
		print(color.BOLD + '#' * 180 + color.END)
		parser.exit()

	user = args.user
	passwd = args.passwd
	csvinfile = args.csvinfile
	switch_list = args.switch
	if switch_list is not None:
		switch = switch_list.split(",")
	else:
		switch = None
	server = args.server

	
	baseuri = "https://{}/cvpservice".format(server)
	auth_data = json.dumps({'userId': user, 'password': passwd})
	auth_url = (baseuri + "/login/authenticate.do")
	auth_resp = requests.post(auth_url,data=auth_data,verify=False)
	cookies = auth_resp.cookies


	if (csvinfile is not None) and (switch is None):
		csvinput()
	elif (switch is not None) and (csvinfile is None):
		cmdflags()
	else:
		parser.print_help()
		print(color.BOLD + '#' * 180 + color.END)
		readme()
		print(color.BOLD + '#' * 180 + color.END)
		parser.exit()


def csvinput():
	switch = []
	with open (csvinfile, 'r') as csvfile:
		reader = csv.DictReader(csvfile)

		for row in reader:
			switch.append(row['switch'])

		hosts = json.dumps({'hosts': switch})
		inventory = (baseuri + "/inventory/devices")
		post_inventory = requests.post(inventory,cookies=cookies,data=hosts,verify=False)
		print(post_inventory.content)


def cmdflags():
	hosts = json.dumps({'hosts': switch})
	inventory = (baseuri + "/inventory/devices")
	post_inventory = requests.post(inventory,cookies=cookies,data=hosts,verify=False)
	print(post_inventory.content)


if __name__ == '__main__':
	main()