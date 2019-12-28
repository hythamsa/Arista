import sys, getpass, ssl, argparse, paramiko, datetime, csv
from jsonrpclib import Server

class color:
    HEADER = '\033[95m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def Arguments():
    parser = argprase.ArgumentParser()
    parser.add_argument("-u", "--user", dest='user', default='admin', help'Username used for switch authenticaion')
    parser.add_argument("-p", "--pass", dest='passwd', help='Password for switch authentication')
    parser.add_argument("-m", "--method", dest='method', help='Select SSL or non-SSL', choices=['http', 'https'])
    parser.add_argument("-e", "--enable", dest='enable', help='Provide an enable password if configured')
    parser.add_argument("-s", "--switch", dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
    parser.add_argument("-up", "--upload", dest='upload', help='Specify binary image to upload. Full path is only required IF script is executed in a different directory where image is stored')
    parser.add_argument("-bn", "--bname", dest='bname', help='Specify the name of the binary image in flash. EG: EOS-4.21.5F')
    parser.add_argument("-po", "--port", dest='port', default='22', help='Specify the SSH port to be used for file transfer', type=int)
    parser.add_argument("-o", "--csvoutfile", dest='csvoutfile', help='Specify the name of the CSV file to output failed upgrades')
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    return verifyargs(args)


def verifyargs():
    if ars.passwd is None:
        args.passwd = getpass.getpass()

    return args


def main():
    # Set today's date
    today = datetime.date.today()

    # Do not verify self-signed certs
    ssl._create_default_https_context = ssl._create_unverified_context

    # Define minimum uptime as 1 week (604800s)
    min_time = 604800

    options = Arguments()

    #Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", dest='user', help='Username used for switch authentication')
    parser.add_argument("-p", "--pass", dest='passwd', help='Password for switch authentication')
    parser.add_argument("-m", "--method", dest='method', help='Select SSL or non-SSL', choices=['http', 'https'])
    parser.add_argument("-e", "--enable", dest='enable', help='Provide an enable password if configured')
    parser.add_argument("-s", "--switch", dest='switch', help='Provide a switch or a list of switches separated by a comma (,). Name or IP address are accepted')
    parser.add_argument("-up", "--upload", dest='upload', help='Specify binary image to upload. Full path is only required IF script is executed in a different directory where image is stored')
    parser.add_argument("-bn", "--bname", dest='bname', help='Specify the name of the binary image in flash. EG: EOS-4.21.5F')
    parser.add_argument("-po", "--port", dest='port', help='Specify the SSH port to be used for file transfer', type=int)
    parser.add_argument("-o", "--csvoutfile", dest='csvoutfile', help='Specify the name of the CSV file to output failed upgrades')
    #parser.add_argument("-ml", "--mlag", dest='mlag', help='Provide switches that are mlag enabled')
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    user = args.user
    passwd = args.passwd
    method = args.method
    enable = args.enable
    switch_list = args.switch
    if switch_list is not None:
        switch = switch_list.split(",")
    else:
        switch = None
    bname = args.bname
    upload = args.upload
    port = args.port
    csvoutfile = args.csvoutfile
    #mlag = args.mlag

    # Alernative password input which will NOT ECHO to terminal and will not display on command line. To use; uncomment the line below:
    #passwd = getpass.getpass()

    # List creation to append valid and failed hosts. failed_upgrade should be turned into a CSV
    perform_upgrade = []
    continue_uptime_check = []
    #failed_upgrade = []

    
    # Verify MLAG status. If MLAG is active, add to CSV. If MLAG not active, then continue to uptime verification
    with open (csvoutfile + '_' + str(today) + '.csv', 'w') as csvfile:
        headers = ['Switch ID', 'MLAG Status', 'Uptime']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for a in switch:
            cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,a))
            get_mlag = cmdapi.runCmds(1,["show mlag"])

            for b in get_mlag:
                mlag_status = b["state"]
                if mlag_status != "active":
                    continue_uptime_check.append(a)
                else:
                    writer.writerow({'Switch ID': a, 'MLAG Status': mlag_status, 'Uptime': "N/A"})
                
                    #failed_upgrade.append({
                    #    "switch": a,
                    #    "mlag": mlag_status
                    #    })

                    print('#' * 48)
                    print(color.RED + color.BOLD + "{} UPGRADE CANNOT PROCEED".format(a) + color.END)
                    print(color.BOLD + "Active MLAG configuration found" + color.END)
                    print('#' * 48)
                    print('')

    # Verify if uptime is greater than 1 week (604800s)
    with open (csvoutfile + '_' + str(today) + '.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        for a in continue_uptime_check:
            cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,a))
            get_uptime = cmdapi.runCmds(1,["show version"])

            # Verify if key 'uptime' exists. Older versions of EOS (EG: 4.20.5.1F) do not have 'uptime' key defined
            if 'uptime' in get_uptime[0]:
                for b in get_uptime:
                    current_uptime = b["uptime"]

                    if current_uptime < min_time:
                        print('#' * 48)
                        print(color.RED + color.BOLD + "{} UPGRADE CANNOT PROCEED".format(a) + color.END)
                        print(color.BOLD + "Uptime is {} < {}".format(current_uptime,min_time) + color.END)
                        print('#' * 48)
                        print('')

                        writer.writerow({'Switch ID': a, 'MLAG Status': "N/A", 'Uptime': current_uptime})

                        #failed_upgrade.append({
                        #    "switch": a,
                        #    "uptime": current_uptime
                        #    })
                    
                    elif current_uptime > min_time:
                        print('#' * 48)
                        print(color.HEADER + color.BOLD + "{} UPGRADE MAY PROCEED".format(a) + color.END)
                        print('#' * 48)
                        print('')
                        perform_upgrade.append(a)


    # When bname is specified on its own WITHOUT upload option, it is assumed that the binary is in flash on switches
    if (upload is None) and (perform_upgrade is not None) and (bname is not None):
        for i in perform_upgrade:
            cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,i))
            update_sw = cmdapi.runCmds(1,["enable", "install source flash:" + bname + " now"])
            print("Upgrading host {} now...".format(i))
            #verify_upgrade = cmdapi.runCmds(1,["show boot"])
            

    # Upload binary into /mnt/flash on to all switches that have passed the checks
    elif (upload is not None) and (perform_upgrade is not None) and (bname is not None):
        for i in perform_upgrade:
            transport = paramiko.Transport((i, port))
            transport.connect(username = user, password = passwd)
            sftp = paramiko.SFTPClient.from_transport(transport)

            print('')
            print('#' * 48)
            print(color.BOLD + "Transferring file {} to {} now".format(upload,i) + color.END)
            print('#' * 48)
            print('')

            sftp.put(upload,"/mnt/flash/" + bname,callback=byte_track)
            sftp.close()
            transport.close()

            print('')
            print('#' * 48)
            print(color.BOLD + "File {} transfer to {} complete".format(upload,i) + color.END)
            print('#' * 48)
            print('')

    
    # Start software update
    for i in perform_upgrade:
        cmdapi = Server("{}://{}:{}@{}/command-api".format(method,user,passwd,i))

        print('')
        print('#' * 60)
        print(color.BOLD + 'Updating {} to {} software image now...'.format(i,bname) + color.END)
        print('#' * 60)
        print('')

        update_sw = cmdapi.runCmds(1,["enable", "install source flash:" + bname + " now"])

        print('')
        print('#' * 60)
        print(color.BOLD + 'Update to revision {} for {} complete'.format(bname,i) + color.END)
        print('#' * 60)
        print('')
    
    # Software image verification
    for i in perform_upgrade:
        print('')
        print('#' * 48)
        print(color.BOLD + 'Boot system check for {} starting now...'.format(i) + color.END)
        print('#' * 48)
        print('')
        verify_boot = cmdapi.runCmds(1,["enable", "show boot"])
        eos_verify = verify_boot[1]['softwareImage']
        boot_sys = eos_verify.strip('flash:/')
        #print(boot_sys,bname)
        if boot_sys == bname:
            print(color.HEADER + 'Code update to {} is successful. Boot set to {}'.format(bname,boot_sys) + color.END)
            print('')
        else:
            print(color.BOLD + color.RED + 'Code update to host {} revision {} failed. Boot set to: {}'.format(i,bname,boot_sys) + color.END)
            print('')


# Used to track upload transfers for the EOS binary
def byte_track(transfer, rem_transfer):
    print(color.BOLD + "Transferred {0} out of {1}".format(transfer, rem_transfer) + color.END)


if __name__ == '__main__':
    main()

    #for j in summ[0]['vrfs']['default']['peers']:
        #prefix = summ[0]['vrfs']['default']['peers'][b]['peerState']   
        #print("\t######### BGP stats for {} #################\n".format(a))
        #if state != "Established":
        #    print("\t\t**** PEER NOT ESTABLISHED ****")
        #    print("\t\tPeer {} State: {}".format(b,state))
        #    print("\t\t******************************\n")
        #else:
        #    print("\t\tPeer {} State: {}\n".format(b,state))