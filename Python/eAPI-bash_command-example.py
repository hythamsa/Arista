#!/usr/bin/python

'''
Basic script highlighting the ability to pass bash shell commands via eAPI
'''

from jsonrpclib import Server
import ssl, getpass

ssl._create_default_https_context = ssl._create_unverified_context


bash_cmd = str(raw_input("BASH Command: "))

proto = str(raw_input("Which eAPI protocol do you want to use [http or https]? "))

input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma: "))
host = input.split(",")

user = str(raw_input("Username: "))
passwd = getpass.getpass()


for a in host:
	cmdapi = Server("%s://%s:%s@%s/command-api" % (proto,user,passwd,a))
	exec_cmd = cmdapi.runCmds(1,["bash timeout 3 " + bash_cmd])

	print '#' * 12, "\t", "%s for %s" % (bash_cmd,a), "\t", '#' * 18
	print exec_cmd[0]['messages'][0]