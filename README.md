# Arista

# Python
A collection of python (duh...) scripts that can be used to retrieve data or for configuring tasks across a single host or multiple hosts

# show-ip-bgp-summary (Python 2.7.x)
Pretty self explanatory. Retrieves a concatenated "sh ip bgp summ" for hosts you select. The script will return the following:
- Peer IP Address
- Peer State
- Prefixes Received
- AS Number of Neighbour
- Up/Down Time of Peer relationship IF established

Username and password are entered on the command line without necessity of modifying script. getpass() used to prevent password echo to terminal
