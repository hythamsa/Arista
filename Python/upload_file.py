#!/usr/bin/python

import paramiko, getpass

local = str(raw_input("Enter name of file to be uploaded: "))
remote_file = str(raw_input("Remote filename: "))
input = str(raw_input("Enter a switch, or switches, to upload to separated by a comma(,): "))
host = input.split(",")
port = int(raw_input("SSH listening port? "))

user = str(raw_input("Username: "))
passwd = getpass.getpass()

for i in host:
	transport = paramiko.Transport((i, port))
	transport.connect(username = user, password = passwd)
	sftp = paramiko.SFTPClient.from_transport(transport)

	sftp.put(local,"/mnt/flash/" + remote_file)
	sftp.close()
	transport.close()