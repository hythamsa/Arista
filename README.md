# Arista

# Python
A collection of python (duh...) scripts that can be used to retrieve data or for configuring tasks across a single host or multiple hosts.

Please note that you will require jsonrpclib in order to execute the scripts.

To install:
- pip install jsonrpclib

# sh-ip-bgp-summ.py (Python 2.7.x)
Pretty self explanatory. Retrieves a concatenated "sh ip bgp summ" for hosts you select allowing the user to display the output directly to their terminal window OR output the data to a CSV file. The script will return the following:

- Switch ID
- Peer IP Address
- Peer State
- Prefixes Received
- AS Number of Neighbour
- Up/Down Time of Peer relationship IF established

Username and password are entered on the command line without necessity of modifying script. getpass() used to prevent password echo to terminal. I didn't see the need to leverage getpass.getuser() to prevent echoing of username in terminal window.

# sh-version.py (Python 2.7.x)
Retrieves versioning information for a host or multiple hosts. The script allows you to select whether output is to be displayed in the terminal or output to a CSV file that I recommend that you use if # of hosts is > 5. Up to you. The script returns the following values:

- Switch ID
- Serial Number
- Model Name
- Software Version
- Uptime

# provision-vlan.py (Python 2.7.x)
Configures a VLAN or mutliple VLANs across a single switch or multiple switches leveraging a CSV file as input or allowing the user to input via the terminal from which the script is run. 

When selecting "csvinput" input, please be sure to input the file name in its entirety including extension and that it is located in the same working directory as the script.
- EG: vlan-config.csv

# sh-error_counters.py (Python 2.7.x)
Retrieves (in/out)put error counters for a single interface, or multiple interfaces on a single switch or multiple switches. Supports output to both CSV and Terminal. If "-c" flag is NOT specified, the script will default to terminal output. If "-c" flag is used, an argument is required for file naming.

In fact, required flags are: -u, -p, -m, -e, -s, & -i

Usage for single interface, single switch:
- ./sh-error_counters.py -u admin -p admin -m http -s leaf1 -i Ethernet49/1

Usage for a single interface, two switches:
- ./sh-error_counters.py -u admin -p admin -m http -s leaf1,leaf2 -i Ethernet49/1

Usage for two interfaces, two switches:
- ./sh-error_counters.py -u admin -p admin -m https -s leaf1,leaf2 -i Ethernet49/1,Ethernet50/1

Usage for two interfaces, one switch:
- ./sh-error_counters.py -u admin -p admin -m http -s leaf1 -i Ethernet49/1,Ethernet50/1 -c Errors

# eAPI-bash_command-example.py (Python 2.7.x)
An incredibly simple script highlighting the ability to pass bash shell commands via eAPI. Please note that when passing shell commands, the timeout (measured in seconds) argument is required.

- EG: "bash timeout 3 df -h"

Example Usage:
- ./eAPI-bash_command-example.py -u admin -p admin -m https -s leaf1,leaf2 -c "df -h"

# provision-l2-vxlan.py (Python 2.7.x)
Makes use of an input CSV to create VXLAN enabled VLANs across an L2 EVPN fabric. For the time being I have not written the script to make use of argprase module to allow for command-line input, so... this will have to do for now.

Following headers in the CSV file are necessary with the exact names (unless you go and modify the script to look for something different):

- switch (this can be a hostname or IP address)
- vlan-id (pretty self explanatory... 2 - 4094)
- vlname (VLAN name)

Flags reqruired for proper operation:
- -u (username)
- -p (password)
- -m (choices: http or https)
- -c (CSV INPUT file name)

Use:
- python provision-l2-vxlan.py -u admin -p admin -m https -c provision-l2-vxlan_INPUT.csv

# delete-l2-vxlan.py (Python 2.7.x)
If you guessed that this will delete VXLAN enabled VLANs (VXeVLs), you win! I use this script in conjunction with the provision-l2-vxlan.py script when working in lab environments to quickly spin up and spin down VXeVLs.

The format of the CSV file is idential to what is described for provision-l2-vxlan.py. Refer to provision-l2-vxlan_INPUT.csv for more info.

Flags reqruired for proper operation:
- -u (username)
- -p (password)
- -m (choices: http or https)
- -c (CSV INPUT file name)

Use:
- python delete-l2-vxlan.py -u admin -p admin -m https -c delete-l2-vxlan_INPUT.csv

# provision-l3-vxlan.py (Python 2.7.x)
Makes use of an input CSV (for now) to create VLANs, SVIs and assigning them to EXISTING VRFs. The format of the CSV (please see vxlan-vlan_INPUT.csv) requires the following headers:

- switch
- vlan-id
- vlan_name
- ip_address
- vrf
- description

The "description" header is used as a description for the SVI interface.

Flags required for proper operation:
- -u (username)
- -p (password)
- -m (choices: http or https)
- -c (CSV INPUT file name)

Use:
- python provision-l3-vxlan.py -u admin -p admin -m http -c provision-l3-vxlan_INPUT.csv

# upgrade_eos.py (Python 2.7.x)
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

To use; uncomment the following line: #passwd = getpass.getpass() . By doing so, you DO NOT NEED TO specify the "-p" flag

Example execution using "-p":
./upgrade.py -u admin -p admin -m https -BN EOS-4.21.5F.swi -s leaf1,leaf2,leaf3

Example execution without use of "-p":
Mac:Python $ ./upgrade.py -u admin -m http -bn EOS-4.21.5F.swi -s leaf1,leaf2,leaf3
Password:

^^Enter password when prompted

# upload_file.py (Python 2.7.x)
Requirements: Paramiko

To install: pip install paramiko

Script allowing user to upload a single file, or multiple files, to your switches & routers defaulting to /mnt/flash as the remote directory. When asked for the "Remote filename"; you are to specify the name of the file as you would like it to appear in the remote directory.

# CVP

A collection of python scripts leveraging the CloudVision Portal API to automate tasks against ... you guessed it... Arista's CloudVision Portal (CVP).

Please note that for some of the scripts you will require CVP API modules installed within your python environment (virtual or otherwise) in order to leverage the scripts contained within this directory. You can find the CVP modules in Arista's software download page within the CloudVision Portal menu.

Other scripts leverage the CVP RESTful API which will be stated (at least that's my intent...if it is not stated, scream at me. It's pretty obvious just by looking at the import modules).

# get_inventory.py (Python 3.x) - leverages REST API
Straightforward. Retrieves a list of inventory from your CVP server dumping the JSON data to your screen... I'll ... uh... need to clean up the returned data to make it presentable. My bad.

Use:
- python3 get_inventory.py -u cvpadmin -p cvpadmin -s <IP address of CVP server>

# post_inventory.py (Python 3.x) - leverages REST API
Module requirements:
- requests
- json
- argparse

To install modules:
pip3 install requests
pip3 install jsonrpclib
pip3 install argparse

Description:
Bulk upload switches into CVP assigned to "undefined" container (for now) using input directly from the command line using the "-s" switch OR using a CSV Input file leveraging "-c"

Please NOTE that you cannot use both "-s" or "-c" at the same time. See usage below

Required Flags:
- -u (username)
- -p (password)
- -sr (CVP FQDN or IP)

Optional Flags:
- -s (switch names or IP addresses separated by a comma (,) )
- -c (CSV file name)

Usage:
- python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -s 10.92.62.47,10.92.62.48,10.92.61.208,10.92.61.207,10.92.61.206,10.92.61.210,10.92.61.205
- python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -c post_inventory_upload.csv
