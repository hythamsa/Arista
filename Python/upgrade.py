#!/usr/bin/python

import sys, getpass, ssl, argparse
from jsonrpclib import Server
from paramiko import SSHClient
#from scp import SCPClient


def main():

    # Do not verify self-signed certs
    ssl._create_default_https_context = ssl._create_unverified_context
    min_time = 604800

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", dest='user', help='Username used for switch authentication')
    parser.add_argument("-p", "--pass", dest='passwd', help='Password for switch authentication')
    parser.add_argument("-m", "--method", dest='method', help='Select SSL or non-SSL', choices=['http', 'https'])
    parser.add_argument("-e", "--enable", dest='enable', help='Provide an enable password if configured')
    parser.add_argument("-s", "--switch", dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
    parser.add_argument("-UP", "--upload", dest='upload', help='Specify a binary image to upload to switches IF one has not been staged on all switches')
    parser.add_argument("-BN", "--bname", dest='bname', help='Specify the name of the binary image to be used located in flash. EG: EOS-4.21.5F')
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    user = args.user
    passwd = args.passwd
    method = args.method
    enable = args.enable
    switch_list = args.switch
    if not switch_list == None:
        switch = switch_list.split(",")
    bname = args.bname
    upload = args.upload


    # Alernative password input which will NOT ECHO to terminal and will not display on command line. Uncomment line 41 to enable non-ECHO/Display
    #passwd = getpass.getpass()


    continue_upgrade = []
    failed_upgrade = []

    for a in switch:
        cmdapi = Server("%s://%s:%s@%s/command-api" % (method,user,passwd,a))
        summ = cmdapi.runCmds(1,["show ip bgp summary"])
        get_uptime = cmdapi.runCmds(1,["show version"])

        for b in get_uptime:
            current_uptime = get_uptime[0]["uptime"]

            if current_uptime < min_time:
                print "\t\t***** %s UPGRADE CANNOT PROCEED *****" % a
                failed_upgrade.append({
                    "switch": a,
                    "uptime": current_uptime
                    })
                print "\t\t%s uptime is %s which is < %s\n" % (a,current_uptime,min_time)

            elif current_uptime > min_time:
                print "\t\t***** %s UPGRADE IS A GO! *****\n" % a
                continue_upgrade.append(a)

    if upload is None:
        for i in continue_upgrade:
            cmdapi = Server("%s://%s:%s@%s/command-api" % (method,user,passwd,i))
            update_sw = cmdapi.runCmds(1,["enable", "install source flash:" + bname + " now"])
            print "Upgrading host %s now..." % i
            verify_upgrade = cmdapi.runCmds(1,["show run section boot"])


if __name__ == '__main__':
    main()
