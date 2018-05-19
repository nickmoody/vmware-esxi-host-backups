#!/usr/bin/env python
# Copyright (C) 2018
# vmware_esxi_host_backup.py
# This script by default will backup VMware ESXI host configurations to a file and if desired copy to TFTP server
# Author - Nick Moody - netassured.co.uk
# Last Updated 19th May 2018
#
# REQUIRMENTS
# 1) VMware VCli installed - https://code.vmware.com/tool/vsphere-cli/6.5
# 2) Intially connect to the host to retrieve the thumbprint
# 3) TFTP server to send the running configs too

# Known limitations:
''' TFTP is not encrypted so only execute this script on a dedicated management network or over a VPN
This script backs up the host configuration only it does not backup the VM's running on the host. You will
need another backup solution for the VM's https://netassured.co.uk/implementing-vm-backup-solution-home-lab/ '''

import time
import os
import sys
import subprocess
import json

# Configuration options

backup_folder = "/backups/vmware/"
tftp_server = '10.10.10.10'
tftp_folder = '/vmware'

# specify the date and time for use in the filename
hour=time.strftime('%H')
minute=time.strftime('%M')
day=time.strftime('%d')
month=time.strftime('%m')
year=time.strftime('%Y')
today=day+"-"+month+"-"+year+"-"+hour+minute

''' Define the list of hosts to be backed up. IP addresses can be used in place of hostnames. For a large a number of hosts
it might be neater to use an external file then import into the script. Replace the thumbprint value with the hash returned 
from the indvidual host. '''

host_01 = {'ip': 'host01', 'username': 'root', 'password': 'password', 'thumbprint': '0C:E9:7D:E9:D6:9A:A9:5B:51:92:5A:DD:0F:4F:75:1F:31:54:1E:79'}
host_02 = {'ip': 'host02', 'username': 'root', 'password': 'password', 'thumbprint': 'BB:59:AE:CD:B6:F0:EC:AA:48:69:60:AE:01:37:3C:B9:04:37:77:9F'}
host_03 = {'ip': 'host03', 'username': 'root', 'password': 'password', 'thumbprint': 'B4:26:72:DF:A0:17:9C:41:52:27:2D:10:46:58:2D:BD:80:69:6A:B7'}

# Create a python list to include which hosts to backup
esxi_hosts = [host_01,host_02,host_03]

# Execute the backup of host(s):

for device in esxi_hosts:

    # Retrieve the values for the host from the dictionary
    host = device['ip']
    username = device['username']
    password = device['password']
    thumbprint =device['thumbprint']
    # Connect to the host and retrieve the version and build number to be applied to the filename
    get_build='esxcli --server'+ ' '+host+' '+'--username'+' '+username+' '+'--password'+' '+password+' '+'--thumbprint'+' '+thumbprint+' '+'--debug --formatter=python system version get'
    os.system(get_build)
    # Capture the output and store as a variable
    get_build_info = subprocess.check_output(get_build, shell=True)
    # convert the varible from a string to a dictionary in json format
    build_info = json.loads(get_build_info)
    # Retrieve the values from the dictionary to be applied to the filename
    version_number = build_info["Version"]
    build_number = build_info["Build"]
    # set the date / time to be applied to the filename
    set_date = today
    # store all the values for use in the filename in one variable
    filename = device['ip']+'_'+today+'_'+version_number+'_'+build_number+'.tgz'
    # prepare the command to be executed against the host to retrieve the config
    save_config='vicfg-cfgbackup --server'+ ' '+host+' '+'-username'+' '+username+' '+'-password'+' '+password+' '+'-s'+' '+backup_folder+filename
    # Execute the command against the host
    os.system(save_config)
    # tftp the file to remote server
    tftp_cmd = 'tftp ' +tftp_server+' << fin'+'\n'+'put '+backup_folder+filename+' '+tftp_folder+'/'+filename+'\n'+'quit'
    os.system(tftp_cmd)
