# Arista

# **Python**
A collection of python (duh...) scripts that can be used to retrieve data or for configuring tasks across a single host or multiple hosts.

Please note that you will require jsonrpclib in order to execute the scripts.

To install:
- pip install jsonrpclib

## [*sh-ip-bgp-summ.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/sh-ip-bgp-summ.py)
Pretty self explanatory. Retrieves a concatenated "sh ip bgp summ" for hosts you select allowing the user to display the output directly to their terminal window OR output the data to a CSV file. The script will return the following:

- Switch ID
- Peer IP Address
- Peer State
- Prefixes Received
- AS Number of Neighbour
- Up/Down Time of Peer relationship IF established

Username and password are entered on the command line without necessity of modifying script. getpass() used to prevent password echo to terminal. I didn't see the need to leverage getpass.getuser() to prevent echoing of username in terminal window.

## [*sh-version.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/sh-version.py)
Retrieves versioning information for a host or multiple hosts. The script allows you to select whether output is to be displayed in the terminal or output to a CSV file that I recommend that you use if # of hosts is > 5. Up to you. The script returns the following values:

- Switch ID
- Serial Number
- Model Name
- Software Version
- Uptime

## [*provision-vlan.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/provision-vlan.py)
Configures a VLAN or mutliple VLANs across a single switch or multiple switches leveraging a CSV file as input or allowing the user to input via the terminal from which the script is run. 

When selecting "csvinput" input, please be sure to input the file name in its entirety including extension and that it is located in the same working directory as the script.
- EG: vlan-config.csv

## [*sh-error_counters.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/sh-errors_counters.py)
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

## [*eAPI-bash_command-example.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/eAPI-bash_command-example.py)
An incredibly simple script highlighting the ability to pass bash shell commands via eAPI. Please note that when passing shell commands, the timeout (measured in seconds) argument is required.

- EG: "bash timeout 3 df -h"

Example Usage:
- ./eAPI-bash_command-example.py -u admin -p admin -m https -s leaf1,leaf2 -c "df -h"

## [*provision-l2-vxlan.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/provision-l2-vxlan.py)
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

## [*delete-l2-vxlan.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/delete-l2-vxlan.py)
If you guessed that this will delete VXLAN enabled VLANs (VXeVLs), you win! I use this script in conjunction with the provision-l2-vxlan.py script when working in lab environments to quickly spin up and spin down VXeVLs.

The format of the CSV file is idential to what is described for provision-l2-vxlan.py. Refer to provision-l2-vxlan_INPUT.csv for more info.

Flags reqruired for proper operation:
- -u (username)
- -p (password)
- -m (choices: http or https)
- -c (CSV INPUT file name)

Use:
- python delete-l2-vxlan.py -u admin -p admin -m https -c delete-l2-vxlan_INPUT.csv

## [*provision-l3-vxlan.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/provision-l3-vxlan.py)
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

## [*upgrade_eos.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/upgrade_EOS.py)
This script was written as a demonstration for a customer looking to automate upgrades based ONLY on switch "uptime". If the switch has not been up for a time
that is equal to or longer than 1 (one) week (604800s), or in an active MLAG domain, the upgrade will not proceed.

I CANNOT even begin to express how simplistic this script is with regards to the lack of any verifcation performed prior to upgrade execution. As stated: it
simply checks "uptime", & MLAG status. NOTHING MORE!


DO NOT:
- automically reload swithches. VERIFY UPGRADE HAS BEEN SUCCESSFUL MANUALLY through "sh boot | json" at minimum (future revisions will take this into account)

This script can be run if:
- switches are fully independent in a non-MLAG pair
- you're ballsy enough to run it on a prod environment. It works exactly as it is written. Nothing more.
- you know how to python, and add verifications beyond the incredibly basic verification check I've implemented post-upgrade. Verification of EOS image

Future revisions:
- write additional pre-checks prior to code execution (BGP, IS-IS, OSPF neighbours)
- write post upgrade verification (only EOS sanity check is performed)
- write MLAG pair determination and sequencing based on: peer-config status fist (if inconsistent, determine partner and skip upgrade for pair). If consistent;
determine MLAG state (active vs disabled), then determine primary vs secondary state, determine link in use, determine partner via LLDP, once determined, perform
upgrade on secondary before moving on to primary
- add arguments check to eliminate the ridiculous need to uncomment for specific functions (I was being stupendously lazy to rush out sample code)

Note regarding password input below:
- I have given you option the to use password input either leveraging the "-p" flag OR one can input directly into terminal where it will not be ECHO'd.

To use; uncomment the following line: #passwd = getpass.getpass() . By doing so, you DO NOT NEED TO specify the "-p" flag

Example execution using "-p":
./upgrade.py -u admin -p admin -m https -BN EOS-4.21.5F.swi -s leaf1,leaf2,leaf3

Example execution without use of "-p":
Mac:Python $ ./upgrade.py -u admin -m http -bn EOS-4.21.5F.swi -s leaf1,leaf2,leaf3
Password:

^^Enter password when prompted

## [*upload_file.py (Python 2.7.x)*](https://github.com/hythamsa/Arista/blob/master/eAPI/upload_file.py)
Requirements: Paramiko

To install: pip install paramiko

Script allowing user to upload a single file, or multiple files, to your switches & routers defaulting to /mnt/flash as the remote directory. When asked for the "Remote filename"; you are to specify the name of the file as you would like it to appear in the remote directory.

# CVP

A collection of python scripts leveraging the CloudVision Portal API to automate tasks against ... you guessed it... Arista's CloudVision Portal (CVP).

Please note that for some of the scripts you will require CVP API modules installed within your python environment (virtual or otherwise) in order to leverage the scripts contained within this directory. You can find the CVP modules in Arista's software download page within the CloudVision Portal menu.

Other scripts leverage the CVP RESTful API which will be stated (at least that's my intent...if it is not stated, scream at me. It's pretty obvious just by looking at the import modules).

## [*get_inventory.py (Python 3.x) - leverages REST API*](https://github.com/hythamsa/Arista/blob/master/CVP/REST%20API/get_inventory.py)
Straightforward. Retrieves a list of inventory from your CVP server dumping the JSON data to your screen... I'll ... uh... need to clean up the returned data to make it presentable. My bad.

Use:
- python3 get_inventory.py -u cvpadmin -p cvpadmin -s <IP address of CVP server>

## [*post_inventory.py (Python 3.x) - leverages REST API*](https://github.com/hythamsa/Arista/blob/master/CVP/REST%20API/post_inventory.py)
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
* -u (username)
* -p (password)
* -sr (CVP FQDN or IP)

Optional Flags:
* -s (switch names or IP addresses separated by a comma (,) )
* -c (CSV file name)

Usage:\
*python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -s 10.92.62.47,10.92.62.48,10.92.61.208,10.92.61.207,10.92.61.206,10.92.61.210,10.92.61.205*\
*python3 post_inventory.py -u cvpadmin -p cvpadmin --server cvp -c post_inventory_upload.csv*\

## [*provision-cvp.py (Python 2.7.x) - leverages CVP API*](https://github.com/hythamsa/Arista/blob/master/CVP/CVP%20API/provision-cvp.py)
The purpose of the script is to create the container topology, and then import switches into their respective containers. You have the option of creating the containers without inventory import, or importing inventory into existing containers without the need to create new containers, and as already stated... creating containers and importing inventory. This will further allow the user to execute container move automatically during script execution or to wait until completion with manual execution.


## *Note:*

* Upon detection of (a) duplicate container(s), or inventory, script will terminate. Error handling to be added in a future revision to allow for continued execution
* Container creation is limited to two levels only as can be seen in the "switch-to-container-provisioning.csv" file. I absolutely plan on correcting this to allow for larger container topology creation
* When assigning a configlet to the container, the saveTopology() will not autoexecute the tasks created to finalize assignment. I've left it manual to allow for proper change controls
* Written in Python 2.7.x 

Supporting CSV input files:\
[Containers CSV](https://github.com/hythamsa/Arista/blob/master/CVP/CVP%20API/provision-container.py)\
[Switch to Container Mappings](https://github.com/hythamsa/Arista/blob/master/CVP/CVP%20API/switch-to-container-provisioning.csv)

Usage:

**Create containers, import switches into their respective container with a compliance check across entire "Tenant":**  
_python provision-cvp.py --user cvpadmin --password arista123 --cvpserver cvp --execute True --container containers.csv --inventory switch-to-container-provisioning.csv_\

Creating Toronto container beneath parent container Tenant\
Creating San Jose container beneath parent container Tenant\
Creating Spines-YYZ container beneath parent container Toronto\
Creating Leaves-YYZ container beneath parent container Toronto\
Creating Spines-SJC container beneath parent container San Jose\
Creating Leaves-SJC container beneath parent container San Jose\
Process completed in 3.40671896935


Importing 10.92.61.205 into container Undefined...\
Process completed in 0.937718868256

Importing 10.92.61.206 into container Leaves-SJC...\
Process completed in 4.14273691177

Importing 10.92.61.207 into container Leaves-YYZ...\
Process completed in 4.1131169796

Importing 10.92.61.208 into container Leaves-YYZ...\
Process completed in 4.3007068634

Importing 10.92.61.210 into container Undefined...\
Process completed in 1.11522197723

Importing 10.92.62.47 into container Spines-YYZ...\
Process completed in 5.31286692619

Importing 10.92.62.48 into container Spines-SJC...\
Process completed in 4.19532990456


**Create containers only:**\
_python provision-cvp.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --container containers.csv --inventory_

**Import switches only:**\
_python provision-cvp.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --inventory switch-to-container-provisioning.csv_

**Upload a static configlet:**\
_python provision-cvp.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --configlet configlets/anycast --configlet_name leafanycast_

**Assign configlet (or configlets) to container and save topology:**\
_python provision-cvp.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --configlet_name leafanycast,trunk --container_name Spines-SJC_


## [*export-devices.py (Python 2.7.x) - leverages CVP API*](https://github.com/hythamsa/Arista/blob/master/CVP/CVP%20API/export-devices.py)
Quickly written for a customer that required device export from Arista CVP (Cloud Vision Platform) into a CSV file for reporting purposes. Please note that when leveraging the "--provisioned" flag it is set to "False" by default. This means that **ALL** onboarded devices will be retrieved from CVP, whereas setting the "--provisioned" flag to "True" will only retrieve provisioned devices. 

Currently the only reported metrics are:
* Hostname
* Serial Number
* Model Number
* EOS Version
* IP Address
* System MAC Address

Of course metrics collected can be adjusted based on your needs.

**Export all onboarded devices (default execution):**\
_python export-devices.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --provisioned False_

**Export only provisioned devices:**\
_python export-devices.py --user cvpadmin --password cvpadmin --cvpserver <CVPSERVER-IP> --provisioned True_

## [*check_compliance.py (Python 2.7.x) - leverages CVP API*](https://github.com/hythamsa/Arista/blob/master/CVP/CVP%20API/check_compliance.py)
This script is only written to resolve device configurations that are out of sync. When executed a compliance check is initiated against all devices in CVP inventory. If devices are found to be out of compliance, a message is dumped to console, and a subsequent reconcile is performed against the Tenant container.

**Sample run:**\
_python check_compliance.py -u cvpadmin -p cvpadmin --cvpserver cvp2019_\
Device "dm1-262sw39.aristanetworks.com" is not in compliance due to Config out of sync\
Device "dm1-262sw40.aristanetworks.com" is not in compliance due to Config out of sync

Reconciliation of all devices completed successfully

_python check_compliance.py -u cvpadmin -p cvpadmin --cvpserver cvp2019_\
All devices are in compliance, and no reconciliation required

**To do:**
* Determine device parent container using retrieveInventory()
* Once I've determined the parent container of each device, I'll initiate reconcileAll=True only on the pertinent containers using reconcileContainer()
* Generate a report, and email distro list or user (whatever customer wants... they can configure it on command line)

## [*ConfigureMLAG.zip (CVP Configlet Builder)*](https://github.com/hythamsa/Arista/blob/master/CVP/Configlet%20Builder/ConfigureMLAG.zip)
Leverages the CVP Configlet Builder tool to dynamically generate MLAG configurations for switch pairs. Download the .zip file, & import directly into CVP to run.

## [*CreateVLAN_and_SVI.zip (CVP Configlet Builder)*](https://github.com/hythamsa/Arista/blob/master/CVP/Configlet%20Builder/CreateVLAN_and_SVI.zip)
Leverages the CVP Configlet Builder tool to dynamically generate a single VLAN configuration along with the option to create an associated SVI if required. Download the .zip file, & import directly into CVP to run.

# **ZTP Server**

Arista's zero touch provisioning model allowing organizations to leverage the power of EOS and LINUX to instantiate a device from scratch without ever having to touch the command line interface.

For a full explanation of each of the directories and their corresponding files can be found here: [Arista ZTP Server](https://ztpserver.readthedocs.io/en/master/overview.html)

The example I have provided will turn-up an entire EVPN VXLAN Symmetric IRB environment comprised of two spine swtiches, 2 leaf swtiches configured in an MLAG domain, and a single orphan leaf switch) from initial boot-up, along with an image upgrade if necessary without once touching the command-line interface. 

Looking at the neighbourdb (misspelled to account for proper Canadian spelling :) ) file you'll notice that there is a slight modification between leaf1/2 topology definitions when contrasted against leaf3. Leaf1/2 leverage the use of correlation between the SystemMac aka NodeID, and the definition file. Whereas leaf3 leverages a topology definition using LLDP signalling to verify accuracy of the topology to push the correct definition file.

# **Ansible**

A collection of Ansible playbooks that of course will evolve over time to accommodate a variety of day-to-day operational tasks for those in the newtork engineering world.

## [*EOS Upgrades*](https://github.com/hythamsa/Arista/tree/master/Ansible/EOS_Upgrades)
Written for a customer demonstrating the ability to perform upgrades against Arista's EOS across an inventory. The playbook gathers basic facts, performs a pre-upgrade check to ensure that the target revision of the EOS image is greater than the EOS image currently installed. Future revisions may further incorporate pre-checks for md5 verification, switch uptime, hadware compatibility, and flash size. Once the one, and only pre-check is completed the playbook will upload the EOS image, and execute a reboot. Once the reboot has been executed the "wait_for" module is initialized attemping to connect to 22/tcp after a 2 minute grace period. When the switch returns eos_facts module is executed to gather facts for post-upgrade verification ensuring the target revision, and what is now installed on the switch match.

**Sample run:**\
_[root@ansibleZTP EOS_Upgrades]# ansible-playbook eos_upgrade.yml --limit=harness_\

PLAY [Upgrade EOS] ***************************************************************************************************

TASK [Collecting Facts] **********************************************************************************************
[WARNING]: default value for `gather_subset` will be changed to `min` from `!config` v2.11 onwards

ok: [host1]
ok: [host2]

TASK [Verify current EOS image against target revision] **************************************************************
ok: [host1]
ok: [host2]

TASK [EOS image upload, and install] *********************************************************************************
ok: [host1]
ok: [host2]

TASK [Reboot switch(es) for new EOS image to take effect] ************************************************************
ok: [host1]
ok: [host2]

TASK [Waiting for switch to come back online] ************************************************************************
ok: [host1 -> localhost]
ok: [host2 -> localhost]

TASK [Collecting post upgrade facts] *********************************************************************************
ok: [host1]
ok: [host2]

TASK [Verify EOS revision matches 4.23.3M] ***************************************************************************
ok: [host1] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [host2] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP ***********************************************************************************************************
host1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
host2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0