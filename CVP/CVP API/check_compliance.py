import cvp, sys, argparse, cvpServices

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
	parser = argparse.ArgumentParser(description="Check compliance of all devices within specificed container")
	parser.add_argument('-u', '--user', dest='user', help='CVP username')
	parser.add_argument('-p', '-passwd', dest='passwd', help='CVP password')
	parser.add_argument('-c', '--cvpserver', dest='cvpserver', help='Name or IP address of CVP server')
	parser.add_argument('--port', dest='port', default='443', type=int, help='Port CVP server is listening on')
	args = parser.parse_args()


	if len(sys.argv[1:]) == 0:
		parser.print_help()
		print('')
		readme()
		print('')
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


def readme():
	print(color.RED + color.BOLD + color.UNDERLINE + 'Example usage to execute compliance check against list of returned devices:' + color.END)
	print('python check-compliance.py -u cvpadmin -p cvpadmin --cvpserver <IP or name of CVP server>\n')


def chkcompliance(cvpauth):

	DEVICE_IN_COMPLIANCE = 0
	DEVICE_CONFIG_OUT_OF_SYNC = 1
	DEVICE_IMAGE_OUT_OF_SYNC = 2
	DEVICE_IMG_CONFIG_OUT_OF_SYNC = 3
	DEVICE_IMG_CONFIG_IN_SYNC = 4
	DEVICE_NOT_REACHABLE = 5
	DEVICE_IMG_UPGRADE_REQD = 6
	DEVICE_EXTN_OUT_OF_SYNC = 7
	DEVICE_CONFIG_IMG_EXTN_OUT_OF_SYNC = 8
	DEVICE_CONFIG_EXTN_OUT_OF_SYNC = 9
	DEVICE_IMG_EXTN_OUT_OF_SYNC = 10
	DEVICE_UNAUTHORIZED_USER = 11

	complianceMsgs = {
   		DEVICE_IN_COMPLIANCE : 'In compliance',
   		DEVICE_CONFIG_OUT_OF_SYNC : 'Config out of sync',
   		DEVICE_IMAGE_OUT_OF_SYNC : 'Image out of sync',
   		DEVICE_IMG_CONFIG_OUT_OF_SYNC : 'Image and Config out of sync',
   		DEVICE_IMG_CONFIG_IN_SYNC : 'Unused',
   		DEVICE_NOT_REACHABLE : 'Device not reachable',
   		DEVICE_IMG_UPGRADE_REQD : 'Image upgrade required',
   		DEVICE_EXTN_OUT_OF_SYNC : 'Extensions out of sync',
   		DEVICE_CONFIG_IMG_EXTN_OUT_OF_SYNC : 'Config, Image and Extensions out of sync',
   		DEVICE_CONFIG_EXTN_OUT_OF_SYNC : 'Config and Extensions out of sync',
   		DEVICE_IMG_EXTN_OUT_OF_SYNC : 'Image and Extensions out of sync',
   		DEVICE_UNAUTHORIZED_USER : 'Unauthorized User',
	}


	getdevices = cvpauth.getDevices()

	nonCompliantDevices = []
	for i in getdevices:
		chk_compliance = cvpauth.deviceComplianceCheck(i)

		if chk_compliance != 0:
			nonCompliantDevices.append({
				"Device": i,
				"Compliance Code": complianceMsgs[chk_compliance]
				})
	
	if nonCompliantDevices:
		for i in nonCompliantDevices:
			device = i['Device']
			message = i['Compliance Code']
			print(color.BOLD + "{} is not in compliance due to {}".format(device,message) + color.END)

		print('')
		print(color.BOLD + "Commencing device reconciliation now..." + color.END)
		get_container = cvpauth.getContainer("Tenant")
		cvpauth.reconcileContainer(get_container,reconcileAll=True)
		print('')
		print(color.BOLD + "Reconciliation of all devices completed successfully" + color.END)
		print('')
	else:
		print('')
		print(color.BOLD + "All devices are in compliance, and no reconciliation required" + color.END)
		print('')

def main():
	options = Arguments()

	cvpauth = cvp.Cvp(options.cvpserver, ssl=True, port=options.port)
	cvpauth.authenticate(options.user,options.passwd)

	#Authentication for cvpServices module
	cvpsvcauth = cvpServices.CvpService(options.cvpserver, ssl=True, port=options.port)
	cvpsvcauth.authenticate(options.user,options.passwd)

	chkcompliance(cvpauth)


if __name__ == '__main__':
	main()