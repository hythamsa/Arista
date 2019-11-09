#!/usr/bin/python

'''
Basic script highlighting the ability to pass bash shell commands via eAPI
'''

from jsonrpclib import Server
import ssl, getpass, argparse, sys

ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", dest='user', help='Username used for switch authentication')
parser.add_argument("-p", "--passwd", dest='passwd', help='Password for switch authentication')
parser.add_argument("-m", "--method", dest='method', help='Select SSL or non-SSL', choices=['http', 'https'])
parser.add_argument("-e", "--enable", action='store', dest='enable', nargs='?', help='Provide an enable password if configured')
parser.add_argument("-s", "--switch", dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
parser.add_argument("-c", "--cmd", dest='cmd', help='Enter the LINUX BASH command to be run')
args = parser.parse_args()

if len(sys.argv[1:]) == 0:
	parser.print_help()
	parser.exit()

user = args.user
passwd = args.passwd
method = args.method
enable = args.enable
switch_list = args.switch
if not switch_list == None:
	switch = switch_list.split(",")
cmd = args.cmd

if enable is None:
	for a in switch:
		cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,a))
		exec_cmd = cmdapi.runCmds(1,["bash timeout 3 " + cmd])

		print('')
		print('#' * 12 + '\t' + 'Executing {} for {} stuff'.format(cmd,a) + '\t' + '#' * 18)
		print(exec_cmd[0]['messages'][0])

elif enable is not None:
	for b in switch:
		cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,b))
		exec_cmd = cmdapi.runCmds(1,["enable","bash time 3 " + cmd])

		print('')
		print('#' * 12 + '\t' + 'Executing {} for {}'.format(cmd,a) + '\t' + '#' * 18)
		print(exec_cmd[1])