# Arista

# Python
A collection of python (duh...) scripts that can be used to retrieve data or for configuring tasks across a single host or multiple hosts.

Please note that you will require jsonrpclib in order to execute the scripts.

To install:
- pip install jsonrpclib

# sh-ip-bgp-summ (Python 2.7.x)
Pretty self explanatory. Retrieves a concatenated "sh ip bgp summ" for hosts you select allowing the user to display the output directly to their terminal window OR output the data to a CSV file. The script will return the following:

- Switch ID
- Peer IP Address
- Peer State
- Prefixes Received
- AS Number of Neighbour
- Up/Down Time of Peer relationship IF established

Username and password are entered on the command line without necessity of modifying script. getpass() used to prevent password echo to terminal. I didn't see the need to leverage getpass.getuser() to prevent echoing of username in terminal window.

# sh-version (Python 2.7.x)
Retrieves versioning information for a host or multiple hosts. The script allows you to select whether output is to be displayed in the terminal or output to a CSV file that I recommend that you use if # of hosts is > 5. Up to you. The script returns the following values:

- Switch ID
- Serial Number
- Model Name
- Software Version
- Uptime

# vlan-config (Python 2.7.x)
Configures a VLAN or mutliple VLANs across a single switch or multiple switches leveraging a CSV file as input or allowing the user to input via the terminal from which the script is run. 

When selecting "csvinput" input, please be sure to input the file name in its entirety including extension and that it is located in the same working directory as the script.
- EG: vlan-config.csv

# ssltest.py (Python 2.7.x)
Just a stupid little script testing out non-verification of ssl self-signed certs

# sh-error_counters.py (Python 2.7.x)
Retrieves (in/out)put error counters for a single interface, or multiple interfaces on a single switch or multiple switches. Output is directly to terminal for now.

Usage for single interface, single switch:
./sh-error_counters.py -u admin -p admin -m http -s leaf1 -i Ethernet49/1

Usage for a single interface, two switches:
./sh-error_counters.py -u admin -p admin -m http -s leaf1,leaf2 -i Ethernet49/1

Usage for two interfaces, two switches:
./sh-error_counters.py -u admin -p admin -m http -s leaf1,leaf2 -i Ethernet49/1,Ethernet50/1

Sample Output for the following:
./sh-error_counters.py -u admin -p admin -m http -s leaf1,leaf2 -i Ethernet49/1,Ethernet50/1

########## Error counters for switch leaf1 interface Ethernet49/1 ##########
                      Total Input Errors: 	  568178
                      Total Runt Frames: 	    568178
                      Total RX Pause Frames: 	0
                      Total FCS Errors: 	    0
                      Total Align Errors: 	  0
                      Total Giant Frames: 	  0
                      Total Symbol Errors: 	  0
                      Total Def Transmits: 	  0
                      Total TX Pause Frames: 	0
                      Total Collisions: 	    0
                      Late Collisions: 	      0


########## Error counters for switch leaf1 interface Ethernet50/1 ##########
                      Total Input Errors: 	  567893
                      Total Runt Frames: 	    567893
                      Total RX Pause Frames: 	0
                      Total FCS Errors: 	    0
                      Total Align Errors: 	  0
                      Total Giant Frames: 	  0
                      Total Symbol Errors: 	  0
                      Total Def Transmits: 	  0
                      Total TX Pause Frames: 	0
                      Total Collisions: 	    0
                      Late Collisions: 	      0
