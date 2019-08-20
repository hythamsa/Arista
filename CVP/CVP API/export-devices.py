import argparse, csv, getpass, time, sys, cvpServices, datetime

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


def Arguments():
	parser = argparse.ArgumentParser(description='Export device inventory to terminal or CSV file')
	parser.add_argument('--user', dest='user', nargs='?', help='CVP Username')
	parser.add_argument('--password', dest='passwd', help='CVP Admin Password')
	parser.add_argument('--cvpserver', dest='cvpserver', help='Name or IP Address of the CVP Server')
	parser.add_argument('--port', dest='port', default='443', type=int, help='Web port service CVP is listening on')
	parser.add_argument('--provisioned', dest='provisioned', default=False, type=bool, choices=[True,False], help='False retrieves all onboarded devices. True retrieves only provisioned devices')
	args=parser.parse_args()

	if len(sys.argv[1:]) == 0:
		parser.print_help()
		parser.exit()

	return verifyargs(args)


def verifyargs(args):
	if args.cvpserver is None:
		args.cvpserver = str(raw_input("What is the name or the IP address of the CVP server? "))

	if args.user is None:
		args.user = str(raw_input("What is the CVP admin username? "))

	if args.passwd is None:
		args.passwd = getpass.getpass()

	return args


def exportdevices(cvpsvcauth,provisioned):
	today = datetime.date.today()

	start = time.time()
	with open('Device Export' + '_' + str(today) + '.csv', 'w') as csvfile:
		headers = ['Hostname', 'Serial Number', 'Model Number', 'EOS Version', 'IP Address', 'System MAC Address']
		writer = csv.DictWriter(csvfile, fieldnames=headers)
		writer.writeheader()

		ret_inventory = cvpsvcauth.getInventory()

		for i in ret_inventory[0]:
			serial = i["serialNumber"]
			model = i["modelName"]
			hn = i["hostname"]
			eos = i["version"]
			ipadd = i["ipAddress"]
			macadd = i["systemMacAddress"]

			writer.writerow({'Hostname': hn, 'Serial Number': serial, 'Model Number': model, 'EOS Version': eos, 'IP Address': ipadd, 'System MAC Address': macadd})

		end = time.time()
		exec_time = end - start

		print(color.HEADER + color.BOLD + "Process completed in {}\n".format(exec_time) + color.END)

def main():
	options = Arguments()

	#Authentication for cvpServices module
	cvpsvcauth = cvpServices.CvpService(options.cvpserver, ssl=True, port=options.port)
	cvpsvcauth.authenticate(options.user,options.passwd)

	exportdevices(cvpsvcauth,options.provisioned)


if __name__ == '__main__':
	main()