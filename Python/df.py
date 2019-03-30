#!/usr/bin/python

'''
Basic script highlighting the ability to pass bash shell commands via eAPI
'''

from jsonrpclib import Server
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

cmdapi = Server("https://admin:admin@leaf1/command-api")
getdf = cmdapi.runCmds(1,["bash timeout 30 df -h"])

print getdf[0]['messages'][0]