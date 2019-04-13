#!/usr/bin/python

'''
This script was written as a demonstration for a customer looking to automate upgrades based ONLY on switch "uptime". If the switch has not been up for a time
that is equal to or longer than 1 (one) week (604800s), upgrade will not proceed.

I CANNOT even begin to express how simplistic this script is with regards to the lack of any verifcation performed prior to upgrade execution. As stated: it
simply checks "uptime". Nothing more.

For the time being the script assumes you have already staged the EOS binary on each switch, though, there is an "upload" flag, I have yet to write the code. Soon.
The name specified under the "BN" flag must match the name of the EOS binary found in "flash:/", and if not, no upgrade proceeds.

DO NOT:

- run this script on switches configured as MLAG pairs (future revisions will take this into account). Want to take down a whole pod/zone... that's how you do it
- automically reload swithches. VERIFY UPGRADE HAS BEEN SUCCESSFUL MANUALLY through "sh boot | json" at minimum (future revisions will take this into account)

This script can be run if:
- switches are fully independent in a non-MLAG pair
- you're ballsy enough to run it on a prod environment. It works exactly as it is written. Nothing more.
- you know how to python, and add verifications

Future revisions:
- write "upload" python code leveraging scp and paramiko (I may write for both key and password auth)
- write additional pre-checks prior to code execution (BGP, IS-IS, OSPF neighbours)
- write post upgrade verification
- write MLAG pair determination and sequencing based on: peer-config status fist (if inconsistent, determine partner and skip upgrade for pair). If consistent;
determine MLAG state (active vs disabled), then determine primary vs secondary state, determine link in use, determine partner via LLDP, once determined, perform
upgrade on secondary before moving on to primary.

Note regarding password input below:
- I have given you option the to use password input either leveraging the "-p" flag OR one can input directly into terminal where it will not be ECHO'd.
Uncomment out line 82 for alternative password input. By doing so, you DO NOT NEED TO specify the "-p" flag

Example execution using "-p":
./upgrade.py -u admin -p admin -m https -BN EOS-4.21.5F.swi -s leaf1,leaf2,leaf3

Example execution without use of "-p":
Mac:Python $ ./upgrade.py -u admin -m http -BN EOS-4.21.5F.swi -s leaf1,leaf2,leaf3
Password:

^^Enter password when prompted

'''

import sys, getpass, ssl, argparse, time
from jsonrpclib import Server


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


    # Alernative password input which will NOT ECHO to terminal and will not display on command line. Uncomment below (line 82) to enable non-ECHO/Display
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

    #for j in summ[0]['vrfs']['default']['peers']:
        #prefix = summ[0]['vrfs']['default']['peers'][b]['peerState']   
        #print "\t######### BGP stats for %s #################\n" % a
        #if state != "Established":
        #    print "\t\t**** PEER NOT ESTABLISHED ****"
        #    print "\t\tPeer %s State: %s" % (b,state)
        #    print "\t\t******************************\n"
        #else:
        #    print "\t\tPeer %s State: %s\n" % (b,state)