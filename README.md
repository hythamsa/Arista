# Arista

# Python
A collection of python (duh...) scripts that can be used to retrieve data or for configuring tasks across a single host or multiple hosts

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
