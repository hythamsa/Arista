#!/bin/bash

basedir=/etc/ansible/Backup/
tdate=`date +%Y_%m_%d`

ansible-playbook -i $basedir/hosts $basedir/config-backup.yml

cd $basedir/backup

if [ ! -d ]
  then
      mkdir $tdate
fi

mv $basedir/backup/*_config.* $basedir/backup/$tdate
