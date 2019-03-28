#!/usr/bin/python

import ssl, argparse, sys, datetime, csv
from jsonrpclib import Server

ssl._create_default_https_context = ssl._create_unverified_context
today = datetime.date.today()

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', dest='user', action='store', help='Username for switch auth')
parser.add_argument('-p', '--password', dest='passwd', action='store', help='Password for switch auth')
parser.add_argument('-m', '--proto', dest='proto', action='store', help='http or https for eAPI connectivity')
parser.add_argument('-e', '--enable', dest='enable', action='store', help='Enable password if configured')
parser.add_argument('-s', '--switch', dest='switch', action='store', help='Enter a switch or list of switches separated by a comma')
parser.add_argument('-i', '--intf', dest='intf', action='store', help='Enter interface(s) to retrive counters separated by a comma')
parser.add_argument('-c', '--csvoutfile', dest='csvoutfile', action='store', help='Output to CSV file. No argument required')

if len(sys.argv[1:]) == 0:
	parser.print_help()
	parser.exit()
args = parser.parse_args()

csvoutfile = args.csvoutfile
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


if csvoutfile is None:

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

			 	def_trans = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["deferredTransmissions"]
			 	txpause = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["txPause"]
			 	collisions = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["collisions"]
			 	late_coll = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["lateCollisions"]


			 	print "\n"
			 	print "\t\tError Counters for Switch %s interface %s:" % (host,a)
				print "==================================================================================\n"
			 	print "\t\t\tTotal Input Errors: \t%s" % totInErrors
			 	print "\t\t\tTotal Runt Frames: \t%s" % runt_frames
			 	print "\t\t\tTotal RX Pause Frames: \t%s" % rxpause
			 	print "\t\t\tTotal FCS Errors: \t%s" % fcs_errors
			 	print "\t\t\tTotal Align Errors: \t%s" % align_errors
			 	print "\t\t\tTotal Giant Frames: \t%s" % giant_frames
			 	print "\t\t\tTotal Symbol Errors: \t%s" % sym_errors
			 	print "\t\t\tTotal Def Transmits: \t%s" % def_trans
			 	print "\t\t\tTotal TX Pause Frames: \t%s" % txpause
			 	print "\t\t\tTotal Collisions: \t%s" % collisions
			 	print "\t\t\tLate Collisions: \t%s" % late_coll
			 	print "\n"
else:
	with open (csvoutfile + '_' + str(today) + '.csv', 'w') as csvfile:
		headers = ['Switch ID', 'Interface', 'Total Input Errors', 'Total Runt Frames', 'Total RX Pause Frames', 'Total FCS Errors', 'Total Alignment Errors', 'Total Giant Frames', 'Total Symbol Errors', 'Total Deferred Transmissions', 'Total TX Pause Frames', 'Total Collisions', 'Total Late Collisions']
		writer = csv.DictWriter(csvfile, fieldnames=headers)
		writer.writeheader()

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

			 		def_trans = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["deferredTransmissions"]
			 		txpause = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["txPause"]
			 		collisions = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["collisions"]
			 		late_coll = get_counters[0]["interfaces"][a]["interfaceCounters"]["outputErrorsDetail"]["lateCollisions"]

			 		writer.writerow({'Switch ID': host, 'Interface': a, 'Total Input Errors': totInErrors, 'Total Runt Frames': runt_frames, 'Total RX Pause Frames': rxpause, 'Total FCS Errors': fcs_errors, 'Total Alignment Errors': align_errors, 'Total Giant Frames': giant_frames, 'Total Symbol Errors': sym_errors, 'Total Deferred Transmissions': def_trans, 'Total TX Pause Frames': txpause, 'Total Collisions': collisions, 'Total Late Collisions': late_coll})
