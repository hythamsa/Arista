import sys,argparse,ssl,csv
from jsonrpclib import Server

def main():
	#Disable SSL self-signed verification
	ssl._create_default_https_context = ssl._create_unverified_context

	parser = argparse.ArgumentParser()
	parser.add_argument('--user', dest='user')
	parser.add_argument('--password', dest='passwd')
	parser.add_argument('--csvinfile', dest='csvinfile')
	parser.add_argument('--method', dest='method', choices=['http', 'https'])
	args = parser.parse_args()

	user = args.user
	passwd = args.passwd
	method = args.method
	csvinfile = args.csvinfile

	with open (csvinfile, 'r') as rf:
		reader = csv.DictReader(rf)
		for row in reader:
			sw = row['switch']
			cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,sw))
			cmdapi.runCmds(1,["enable", "configure", "no daemon TerminAttr"])
			shdaemon = cmdapi.runCmds(1,["show daemon"])

			#Verify daemon has been removed from each switch
			print(shdaemon[0]['daemons'])


if __name__ == '__main__':
	main()