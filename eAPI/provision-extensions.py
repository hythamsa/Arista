#!/usr/bin/python

import paramiko, getpass, sys, argparse, ssl, time
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

def arguments():
	parser = argparse.ArgumentParser(description='Upload swix files into switches')
	parser.add_argument('-u','--user', dest='user', default='admin', help='Switch username')
	parser.add_argument('-p','--password', dest='passwd', help='Switch password')
	parser.add_argument('-e','--enable', dest='enable', help='Switch enable password if any')
	parser.add_argument('-s','--switch', dest='switch', help='List of switch names or IP addresses separated by a comma')
	parser.add_argument('-pt','--protocol', dest='protocol', choices=['http', 'https'], default='https', help='Protocol used to connect to eAPI')
	parser.add_argument('-f','--file', dest='filename', help='Name of extension to be uploaded into switch')
	parser.add_argument('--port', dest='port', default='22', type=int, help='Destination port for sFTP transfer')
	args = parser.parse_args()

	if len(sys.argv[1:]) == 0:
		parser.print_help()
		print('')
		readme()
		print('')
		parser.exit()

	return verify(args)


def verify(args):
	if args.passwd is None:
		args.passwd = getpass.getpass()

	return args


def upload(user,passwd,port,switch,filename):
	sw = switch.split(',')

	for a in sw:
		transport = paramiko.Transport((a, port))
		transport.connect(username = user, password = passwd)
		sftp = paramiko.SFTPClient.from_transport(transport)

		print('')
		print('#' * 48)
		print(color.BOLD + "Transferring file {} to {} now".format(filename,a) + color.END)
		print('#' * 48)
		print('')

		sftp.put(filename,"/tmp/" + filename,callback=byte_track,confirm=True)
		sftp.close()
		transport.close()

		print('')
		print('#' * 48)
		print(color.BOLD + "File {} to {} complete".format(filename,a) + color.END)
		print('#' * 48)
		print('')


def extInstall(switch,filename,protocol,user,passwd):
	sw = switch.split(',')

	for a in sw:
		cmdapi = Server("{}://{}:{}@{}/command-api".format(protocol,user,passwd,a))
		#Copy extension from /tmp to extension, then install, and write to memory
		cmdapi.runCmds(1,["enable", "configure", "copy file:/tmp/" + filename + " extension:", "extension " + filename])
		cmdapi.runCmds(1,["enable", "configure", "copy installed-extensions boot-extension", "wr mem"])


def byte_track(transfer,rem_transfer):
	print "Transferred {0} out of {1}".format(transfer,rem_transfer)


def main():
	# Non-verfication of self-signed certificate - BAD
	ssl._create_default_https_context = ssl._create_unverified_context

	opts = arguments()

	#Perform file upload to each switch
	upload(opts.user,opts.passwd,opts.port,opts.switch,opts.filename)

	#Execute Extension Installation
	extInstall(opts.switch,opts.filename,opts.protocol,opts.user,opts.passwd)

if __name__ == '__main__':
	main()