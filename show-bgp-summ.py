#!/usr/bin/python

import sys
from jsonrpclib import Server

user = "admin"
passwd = "admin"

try:
    cmdapi = Server("http://%s:%s@leaf1/command-api" % (user,passwd))
    summ = cmdapi.runCmds(1,["show ip bgp summary"])

    for i in summ[0]['vrfs']['default']['peers']:
        peers = summ[0]['vrfs']['default']['peers'][i]
        state = summ[0]['vrfs']['default']['peers'][i]['peerState']
        prfxrcvd = summ[0]['vrfs']['default']['peers'][i]['prefixReceived']
        asnum = summ[0]['vrfs']['default']['peers'][i]['asn']
        updown = summ[0]['vrfs']['default']['peers'][i]['upDownTime']

        print "\tPeer IP Address: %s" % i
        print "\tPeer State: %s" % state
        print "\tPrefixes Received: %s" % prfxrcvd
        print "\tAS Number: %s" % asnum
        print "\tUP/Down Time: %s\n" % updown

except:
    sys.exit(2)
