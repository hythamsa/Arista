#!/usr/bin/python

import paramiko, getpass

def main():

	file_list = []
	entries = int(raw_input("How many files would you like to upload? "))

	for i in range(entries):
		local_file = str(raw_input("Enter the name of the file to be uploaded: "))
		remote_file = str(raw_input("Remote filename: "))

		file_list.append({
			"loc": local_file,
			"rem": remote_file
			})

	input = str(raw_input("Enter a switch, or switches, to upload to separated by a comma(,): "))
	host = input.split(",")
	port = int(raw_input("SSH listening port? "))

	user = str(raw_input("Username: "))
	passwd = getpass.getpass()

	for a in file_list:
		lf = a['loc']
		rf = a['rem']

		for b in host:
			transport = paramiko.Transport((b, port))
			transport.connect(username = user, password = passwd)
			sftp = paramiko.SFTPClient.from_transport(transport)

			sftp.put(lf,"/mnt/flash/" + rf,callback=byte_track,confirm=True)
			sftp.close()
			transport.close()

def byte_track(transfer, rem_transfer):
	print "Transferred {0} out of {1}".format(transfer, rem_transfer)

if __name__ == '__main__':
	main()