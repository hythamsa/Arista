#!/usr/bin/python

import ssl, argparse
from jsonrpclib import Server

ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', dest='user', action='store', help='Username for switch auth')
parser.add_argument('-p', '--password', dest='passwd', action='store', help='Password for switch auth')
parser.add_argument('-m', '--proto', dest='proto', action='store', help='http or https for eAPI connectivity')
parser.add_argument('-e', '--enable', dest='enable', action='store', help='Enable password if configured')
parser.add_argument('-s', '--switch', dest='switch', action='store', help='Enter a switch or list of switches separated by a comma')
parser.add_argument('-i', '--intf', dest='intf', action='store', help='Enter interface(s) to retrive counters separated by a comma')
args = parser.parse_args()

user = args.user
password = args.passwd
proto = args.proto
enable = args.enable
switch = args.switch
intf = args.intf

switch_list = args.switch
switch = switch_list.split(",")

intf_list = args.intf
intf = intf_list.split(",")

for host in switch:
	cmdapi = Server("%s://%s:%s@%s/command-api" % (proto,user,password,host))
	for a in intf:
		get_counters = cmdapi.runCmds(1,["show interfaces " + a])

		for b in get_counters:

			 totInErrors = get_counters[0]["interfaces"][a]["interfaceCounters"]["totalInErrors"]
			 runt_frames = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["runtFrames"]
			 rxpause = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["rxPause"]
			 fcs_errors = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["fcsErrors"]
			 align_errors = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["alignmentErrors"]
			 giant_frames = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["giantFrames"]
			 sym_errors = get_counters[0]["interfaces"][a]["interfaceCounters"]["inputErrorsDetail"]["symbolErrors"]



			 print "########## Error counters for switch %s interface %s ##########" % (host,a)
			 print "\tTotal Input Errors: \t%s" % totInErrors
			 print "\tTotal Runt Frames: \t%s" % runt_frames
			 print "\tTotal RX Pause Frames: \t%s" % rxpause
			 print "\tTotal FCS Errors: \t%s" % fcs_errors
			 print "\tTotal Align Errors: \t%s" % align_errors
			 print "\tTotal Giant Frames: \t%s" % giant_frames
			 print "\tTotal Symbol Errors: \t%s" % sym_errors
			 print "\n"