#!/bin/bash

# Run backup playbook, and separate into timestamped directory

tdate=`date +%Y_%m_%d`
basedir=/etc/ansible/Backup/

ansible-playbook -i $basedir/hosts $basedir/config-backup.yml  


#Move files into respective directory
cd $basedir/backup

if [ ! -d $tdate ]
	then
		mkdir $tdate
fi

mv $basedir/backup/*_config.* $basedir/backup/$tdate
