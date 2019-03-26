#!/usr/bin/python
  
import sys, getpass, csv
from jsonrpclib import Server

user = str(raw_input("Username: "))
passwd = getpass.getpass()

while True:
    try:
        method = str(raw_input("Which input method will you use [term/csvinput]? "))
    except ValueError:
        print ("Please enter term or csvinput")
        continue
    if (method == "csvinput"):
        filename = str(raw_input("What is the name of your csvfile (Please append with .csv)? "))
        break
    if (method == "term"):
        # Request switch name or IP addresses to be configured
        input = str(raw_input("What switch or switches would you like to connect to separated by a comma: "))
        host = input.split(",")

        # Create empty list, ask user to define total # of entries to be made, append to list
        user_list = []
        entries = int(raw_input("How many entries do you require? "))

        for i in range(entries):
            user_vlanid = str(raw_input("What is the VLAN ID? "))
            user_vlanname = str(raw_input("What is the VLAN name? "))

            user_list.append({
                "vlanid": user_vlanid,
                "vlanname": user_vlanname
                })
        break


def main():
    if method == "term":
        term()
    if method == "csvinput":
        csvinput()

def term():
    for i in user_list:
        vlid = i['vlanid']
        vname = i['vlanname']

        for a in host:
            cmdapi = Server("http://%s:%s@%s/command-api" % (user,passwd,a))
            vlconf = cmdapi.runCmds(1,["enable", "configure", "vlan " + vlid, "name " + vname])

def csvinput():
    try:
        with open (filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                host = row['hosts']
                vlid = row['vlan-id']
                vname = row['vlname']

                for a in host:
                    cmdapi = Server("http://%s:%s@%s/command-api" % (user,passwd,host))
                    vlconf = cmdapi.runCmds(1,["enable", "configure", "vlan " + vlid, "name " + vname])
    except:
        sys.exit(2)

if __name__ == '__main__':
    main()
