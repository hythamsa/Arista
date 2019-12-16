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

def readme():
	print(color.HEADER + color.BOLD + 'Python 2.7.x\n' + color.END)
	print(color.RED + color.BOLD + color.UNDERLINE + 'Required:' + color.END)
	print('Python 2')
	print('paramiko')
	print('argparase')
	#print('cvp')
	#print('cvpServices')
	print('getpass\n')


def Arguments():
	parser = argparse.ArgumentParser(description='Upload swix files into switches')
	parser.add_argument('--swuser', dest='user', default='admin', help='Switch username')
	parser.add_argument('--swpassword', dest='passwd', help='Switch password')
	parser.add_argument('--enable', dest='enable', help='Switch enable password if any')
	parser.add_argument('--csvinfile', dest='csvinfile', help='Name of the CSV input file containing swith names or IP addresses')
	parser.add_argument('--switch', dest='switches', help='List of switch names or IP addresses separated by a comma')
	parser.add_argument('--protocol', dest='protocol', choices=['http', 'https'], default='https', help='Protocol used to connect to eAPI and CVP')
	args = parser.parse_args()

	if len(sys.argv[1:]) == 0:
		parser.print_help()
		print('')
		readme()
		print('')
		parser.exit()

	return verifyargs(args)


def verifyargs(args):
	if args.passwd is None:
		args.passwd = getpass.getpass()

	return args


def main():
	options = Arguments()


if __name__ == '__main__':
	main()