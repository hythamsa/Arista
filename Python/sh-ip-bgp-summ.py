#!/usr/bin/python

import sys, getpass, datetime, csv, ssl
from jsonrpclib import Server


def main():
    while True:
        try:
            choice = str(raw_input("How would you like your data output [csvout/term]? "))
        except ValueError:
            print ("Please enter csvout or term")
            continue
        if (choice == "csvout") or (choice == "term"):
            break
        else:
            print ("Please enter csvout or term")

    if choice == "csvout":
        csvout()
    if choice == "term":
        term()


def csvout():
    today = datetime.date.today()
    ssl._create_default_https_context = ssl._create_unverified_context

    user = str(raw_input("Username: "))
    passwd = getpass.getpass()


    while True:
        try:
            prot = str(raw_input("Which eAPI protocol do you want to use [http or https]? "))
            break
        except ValueError:
            print ("Please enter http or https")
            continue

    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma: "))
    host = input.split(",")

    try:
        with open ('BGP-Summary' + '_' + str(today) + '.csv', 'w') as csvfile:
            headers = ['Switch ID', 'Peers', 'BGP State', 'Prefix(es) Received', 'AS Number', 'Up/Down Status']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for a in host:
                cmdapi = Server("%s://%s:%s@%s/command-api" % (prot,user,passwd,a))
                bgpsumm = cmdapi.runCmds(1,["show ip bgp summary"])

                for b in bgpsumm[0]['vrfs']['default']['peers']:
                    state = bgpsumm[0]['vrfs']['default']['peers'][b]['peerState']
                    prfxrcvd = bgpsumm[0]['vrfs']['default']['peers'][b]['prefixReceived']
                    asnum = bgpsumm[0]['vrfs']['default']['peers'][b]['asn']
                    updown = bgpsumm[0]['vrfs']['default']['peers'][b]['upDownTime']

                    # Write to CSV File
                    writer.writerow({'Switch ID': a, 'Peers': b, 'BGP State': state, 'Prefix(es) Received': prfxrcvd, 'AS Number': asnum, 'Up/Down Status': updown})
    except:
        sys.exit(2)


def term():
    ssl._create_default_https_context = ssl._create_unverified_context

    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    while True:
        try:
            prot = str(raw_input("Which eAPI protocol do you want to use [http or https]? "))
            break
        except ValueError:
            print ("Please enter http or https")
            continue

    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma(,): "))
    host = input.split(",")

    try:
        for a in host:
            cmdapi = Server("%s://%s:%s@%s/command-api" % (prot,user,passwd,a))
            summ = cmdapi.runCmds(1,["show ip bgp summary"])

            for b in summ[0]['vrfs']['default']['peers']:
                state = summ[0]['vrfs']['default']['peers'][b]['peerState']
                prfxrcvd = summ[0]['vrfs']['default']['peers'][b]['prefixReceived']
                asnum = summ[0]['vrfs']['default']['peers'][b]['asn']
                updown = summ[0]['vrfs']['default']['peers'][b]['upDownTime']
            
                print "\t######### BGP stats for %s #################" % a
                print "\tPeer IP Address: %s" % b
                print "\tPeer State: %s" % state
                print "\tPrefixes Received: %s" % prfxrcvd
                print "\tAS Number: %s" % asnum
                print "\tUP/Down Time: %s\n" % updown
    except:
        sys.exit(2)


if __name__ == '__main__':
    main()
