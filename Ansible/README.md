# **Ansible**

A collection of Ansible playbooks that of course will evolve over time to accommodate a variety of day-to-day operational tasks for those in the newtork engineering world.

## [*Backup*](https://github.com/hythamsa/Arista/tree/master/Ansible/Backup)
Simple configuration backup playbook employing the use of a shell script to execute playbook, create directories, and move configuration files into their respective folder date."backup" directory is created by the ansible playbook automagically

**Sample run:**\
[root@ansibleZTP Backup]# ./config-backup.sh

PLAY [Configuration Backup] ******************************************************************************************************************************************************************************************************************

TASK [Backup all EOS configurations] *********************************************************************************************************************************************************************************************************\
changed: [spine1]\
changed: [leaf2]\
changed: [leaf3]\
changed: [leaf1]\
changed: [spine2]\
changed: [host2]\
changed: [host1]

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************\
host1                      : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
host2                      : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
leaf1                      : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
leaf2                      : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
leaf3                      : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
spine1                     : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
spine2                     : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


[root@ansibleZTP backup]# ls -l\
total 0\
drwxr-xr-x 2 root root 288 Apr 28 23:12 2020_04_28

[root@ansibleZTP 2020_04_28]# ls -l\
total 48\
-rw-r--r-- 1 root root 3437 Apr 28 23:12 host1_config.2020-04-28@23:12:03\
-rw-r--r-- 1 root root 4619 Apr 28 23:12 host2_config.2020-04-28@23:12:02\
-rw-r--r-- 1 root root 6596 Apr 28 23:11 leaf1_config.2020-04-28@23:11:56\
-rw-r--r-- 1 root root 6598 Apr 28 23:11 leaf2_config.2020-04-28@23:11:56\
-rw-r--r-- 1 root root 6173 Apr 28 23:11 leaf3_config.2020-04-28@23:11:55\
-rw-r--r-- 1 root root 4171 Apr 28 23:11 spine1_config.2020-04-28@23:11:55\
-rw-r--r-- 1 root root 4005 Apr 28 23:11 spine2_config.2020-04-28@23:11:55


## [*Basic Config Push*](https://github.com/hythamsa/Arista/tree/master/Ansible/Basic_Config_Push)
Written for a customer to quickly demonstrate how one may leverage Ansible to push a template running-configuration to a switch, or multiple switches within your inventory.

Looking more closely at the config_push.yml file you'll notice that I've widely deployed the use of tags (you'll see this across all of my playbooks). If you're not familiar with Ansible playbooks, and their execution the tasks in a playbook are executed in sequential order. By leveraging "tags" this allows me to uniquely identify, and execute a single task, and/or a group of tasks in a playbook without the need to execute the entire playbook in order. I can now either push new configurations, or remove them based on the task I execute.

**Sample run:**\
_ansible-playbook config_push.yml --tags push_template --limit=harness_

The above will execute all tasks tagged with "push_template", and further limit its execution to hosts found within the "harness" group in the inventory

_ansible-playbook config_push.yml --tags delete_template --limit=harness_

The above will execute all tasks tagged with "delete_template", and further limit its execution to hosts found with the "harness" group in the inventory



## [*EOS Upgrades*](https://github.com/hythamsa/Arista/tree/master/Ansible/EOS_Upgrades)
Written for a customer demonstrating the ability to perform upgrades against Arista's EOS across an inventory. The playbook gathers basic facts, performs a pre-upgrade check to ensure that the target revision of the EOS image is greater than the EOS image currently installed. Future revisions may further incorporate pre-checks for md5 verification, switch uptime, hadware compatibility, and flash size. Once the one, and only pre-check is completed the playbook will upload the EOS image, and execute a reboot. When the reboot of the switch is initiated, the "wait_for" module is initialized attemping to connect to port 22/tcp after a 2 minute grace period. When the switch returns eos_facts module is executed to gather facts for post-upgrade verification ensuring the target revision that is now installed on the switch is correct.

**Sample run:**\
_ansible-playbook eos_upgrade.yml --limit=harness_

PLAY [Upgrade EOS] ***************************************************************************************************

TASK [Collecting Facts] **********************************************************************************************\
ok: [host1]\
ok: [host2]

TASK [Verify current EOS image against target revision] **************************************************************\
ok: [host1]\
ok: [host2]

TASK [EOS image upload, and install] *********************************************************************************\
ok: [host1]\
ok: [host2]

TASK [Reboot switch(es) for new EOS image to take effect] ************************************************************\
ok: [host1]\
ok: [host2]

TASK [Waiting for switch to come back online] ************************************************************************\
ok: [host1 -> localhost]\
ok: [host2 -> localhost]

TASK [Collecting post upgrade facts] *********************************************************************************\
ok: [host1]\
ok: [host2]

TASK [Verify EOS revision matches 4.23.3M] ***************************************************************************\
ok: [host1] => {
    "changed": false,
    "msg": "All assertions passed"
}\
ok: [host2] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP ***********************************************************************************************************\
host1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0\
host2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

## [*Deploy AnyCast GW*](https://github.com/hythamsa/Arista/tree/master/Ansible/DeployAnyCastGW)
Written for my EVPN lab environment to quickly deploy, and remove anycast gateways.

Looking more closely at the [anycast_config.j2](https://github.com/hythamsa/Arista/blob/master/Ansible/DeployAnyCastGW/templates/anycast_config.j2) there is some minor intelligence built into the template that will look for the "item.vrf" variable in the [anycast_.yml](https://github.com/hythamsa/Arista/blob/master/Ansible/DeployAnyCastGW/vars_files/anycast.yml) vars file. If configured, then vrf forwarding will be configured on the interface, and if not a standard L3 interface is configured without vrf forwarding


**Sample run:**\
_ansible-playbook anycast_play.yml --tags anycast --limit=leaf_