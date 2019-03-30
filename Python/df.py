#!/usr/bin/python

'''
Basic script highlighting the ability to pass bash commands via eAPI
'''


from jsonrpclib import Server
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

cmdapi = Server("https://admin:admin@leaf1/command-api")
getver = cmdapi.runCmds(1,["bash timeout 30 df -h"])

print getver[0]['messages'][0]