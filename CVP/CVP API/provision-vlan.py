import argparse, sys, cvp, cvpServices, getpass

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
	parser = argparse.ArgumentParser(description='Provision VLANs across multipile switches within a container')
	parser.add_argument('-u', '--user', dest='user', nargs='?', help='CVP username')
	parser.add_argument('-p', '--passwd', dest='passwd', help='CVP passwd')
	parser.add_argument('-c', '--container', dest='container', help='Name of container')
	parser.add_argument('--cvpserver', dest='cvpserver', help='Name of IP address of the CVP server')
	parser.add_argument('--port', dest='port', default='443', type=int, help='Web port service CVP is listening on')
	args = parser.parse_args()

	if len(sys.argv[1:]) == 0:
		parser.print_help()
		print('')
		#readme()
		print('')
		parser.exit()

	return verifyargs(args)


def verifyargs(args):
	if args.user is None:
		args.user = str(raw_input("What is the CVP username? "))

	if args.passwd is None:
		args.passwd = getpass.getpass()

	if args.cvpserver is None:
		args.cvpserver = str(raw_input("What is the name of the IP address of the CVP server? "))

	return args


def getDevicesInContainer(cvpauth,cvpsvcauth,container):

	#Acquire container keyID
	ck = cvpsvcauth.searchContainer(container)
	ck = ck[0]['Key']

	#Retrieve devices under specified container
	ret = cvpsvcauth.getDevicesInContainer(ck,container)
	for i in ret:
		mac = i['netElementKey']
		getDeviceIP(cvpauth,mac)


def getDeviceIP(cvpauth,mac):
	getIP = cvpauth.getDevice(mac)
	print(getIP)


def main():
	options = Arguments()

	#Authentication for cvpServices module
	cvpsvcauth = cvpServices.CvpService(options.cvpserver, ssl=True, port=options.port)
	cvpsvcauth.authenticate(options.user,options.passwd)

	#Authentication for cvp module
	cvpauth = cvp.Cvp(options.cvpserver, ssl=True, port=options.port)
	cvpauth.authenticate(options.user, options.passwd)

	getDevicesInContainer(cvpauth,cvpsvcauth,options.container)


if __name__ == '__main__':
	main()