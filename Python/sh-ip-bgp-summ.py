#!/usr/bin/python

import sys, getpass, datetime, csv
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
    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    today = datetime.date.today()

    input = str(raw_input("What host or hosts would you like to connect to separated by a comma: "))
    host = input.split(",")

    try:
        with open ('BGP-Summary' + '_' + str(today) + '.csv', 'w') as csvfile:
            headers = ['Switch ID', 'Peers', 'BGP State', 'Prefix(es) Received', 'AS Number', 'Up/Down Status']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for a in host:
                cmdapi = Server("http://%s:%s@%s/command-api" % (user,passwd,a))
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
    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma(,): "))
    host = input.split(",")

    try:
        for a in host:
            cmdapi = Server("http://%s:%s@%s/command-api" % (user,passwd,a))
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
