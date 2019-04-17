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

    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma: "))
    host = input.split(",")

    while True:
        try:
            prot = str(raw_input("Which eAPI protocol do you want to use [http or https]? "))
            break
        except ValueError:
            print ("Please enter http or https")
            continue

    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    try:
        with open ('Version' + '_' + str(today) + '.csv', 'w') as csvfile:
            headers = ['Switch ID', 'Serial', 'Model', 'Software Version', 'Up Time']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for a in host:
                cmdapi = Server("%s://%s:%s@%s/command-api" % (prot,user,passwd,a))
                getver = cmdapi.runCmds(1,["show version"])

                serial = getver[0]["serialNumber"]
                model = getver[0]["modelName"]
                swver = getver[0]["version"]
                uptime = getver[0]["uptime"]

                writer.writerow({'Switch ID': a, 'Serial': serial, 'Model': model, 'Software Version': swver, 'Up Time': uptime})
    except:
        sys.exit(2)


def term():
    ssl._create_default_https_context = ssl._create_unverified_context
    
    input = str(raw_input("What switch, or switches, would you like to connect to separated by a comma: "))
    host = input.split(",")

    while True:
        try:
            prot = str(raw_input("Which eAPI protocol do you want to use [http or https]? "))
            break
        except ValueError:
            print ("Please enter http or https")
            continue

    user = str(raw_input("Username: "))
    passwd = getpass.getpass()

    try:
        for a in host:
            cmdapi = Server("%s://%s:%s@%s/command-api" % (prot,user,passwd,a))
            getver = cmdapi.runCmds(1,["show version"])

            for b in getver:
                ser = getver[0]["serialNumber"]
                model = getver[0]["modelName"]
                swver = getver[0]["version"]
                uptime = getver[0]["uptime"]

                print "######### Version Data for %s #################" % a
                print "\tSerial Number: \t%s" % ser
                print "\tModel Number: \t%s" % model
                print "\tSW Version: \t%s" % swver
                print "\tUp Time: \t%s" % uptime
    except:
        sys.exit(2)


if __name__ == '__main__':
    main()
