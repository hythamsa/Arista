#!/usr/bin/python

import sys, getpass, csv, ssl
from jsonrpclib import Server



def main():
    while True:
        try:
            method = str(raw_input("Which input method will you use [term/t or csvinput/c]? "))
            break
        except ValueError:
            print ("Please enter term/t or csvinput/c")
            continue

    if (method == "term") or (method == "t"):
        term()
    if (method == "csvinput") or (method == "c"):
        csvinput()


def term():
    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    ssl._create_default_https_context = ssl._create_unverified_context

    # Request switch name or IP addresses to be configured
    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma: "))
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

        for i in user_list:
            vlid = i['vlanid']
            vlan_name = i['vlanname']

            for a in host:
                cmdapi = Server("https://%s:%s@%s/command-api" % (user,passwd,a))
                vlconf = cmdapi.runCmds(1,["enable", "configure", "vlan " + vlid, "name " + vlan_name])


def csvinput():
    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    ssl._create_default_https_context = ssl._create_unverified_context

    while True:
        try:
            filename = str(raw_input("What is the name of your csvfile (Please append with .csv)? "))
            if filename.lower().endswith('.csv'):
                break
            else:
                print ("Please enter filename ending with .csv")
                continue
        except:
            sys.exit(2)

    with open (filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            host = row['hosts']
            vlid = row['vlan-id']
            vname = row['vlname']

            for a in host:
                cmdapi = Server("https://%s:%s@%s/command-api" % (user,passwd,host))
            #   intfconf = cmdapi.runCmds(1,["enable", "configure", "interface " + intf, "description " + descr, "no switchport", "ip address " + ip])
                vlconf = cmdapi.runCmds(1,["enable", "configure", "vlan " + vlid, "name " + vname])


if __name__ == '__main__':
    main()
