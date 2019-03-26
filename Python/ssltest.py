#!/usr/bin/python

'''
testing out acceptance of self-signed certificates
'''

from jsonrpclib import Server
from pprint import pprint
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

cmdapi = Server("https://admin:admin@leaf1/command-api")
getver = cmdapi.runCmds(1,["show version"])

pprint(getver)