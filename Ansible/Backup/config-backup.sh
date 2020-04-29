#!/bin/bash

basedir=/etc/ansible/Arista/Backup
tdate=`date +%Y_%m_%d`

ansible-playbook -i $basedir/inventory $basedir/config-backup.yml

cd $basedir/backup

if [ ! -d $tdate ]
  then
      mkdir $tdate
fi

mv $basedir/backup/*_config.* $basedir/backup/$tdate