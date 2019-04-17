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


# provision-vxlan-vlan.py (Python 2.7.x)
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
- ./provision-vxlan-vlan.py -u admin -p admin -m http -c vxlan-vlan_INPUT.csv

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
