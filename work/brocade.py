#!/usr/bin/python3

import sys
import paramiko
import datetime
from paramiko import SSHClient, AutoAddPolicy
from paramiko import client

# declare hostnames (ensure DNS updated).temp use IP
brocade_host = 'brocade01.dc.mgmt'
ftp_host = 'ntapocumftp.dc.mgmt'
brocade_usr = 'switchmon'
ftp_usr = 'sysmon'

# parsing as arguments to make script ansible friendly
print ("This is the name of the script: ",sys.argv[0])
print ("To run script: ./brocade_arg.py <switch_pwd> <ftp_pwd>")

brocade_pwd = sys.argv[1]
ftp_pwd = sys.argv[2]

# declare variables
now = datetime.datetime.now()
log_time = now.strftime("%Y%m%d%H%M%S")                                                                                                                                                                                                                                                                   
out_time = "config-" + log_time + ".txt"

# start the script
print("Script executed at", log_time)

#print(brocade_host, brocade_usr, brocade_pwd)
#upload = 'configupload -all -ftp, str(ftp_host), str(ftp_usr), out_time, str(ftp_pwd)'
upload = 'configupload -all -ftp %s,%s,%s,%s' % (ftp_host, ftp_usr, out_time, ftp_pwd)

# ssh to brocade switch
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

#print('ssh.connect', brocade_host, brocade_usr, brocade_pwd )
ssh.connect(brocade_host, username=brocade_usr, password=brocade_pwd)

stdin, stdout, stderr = ssh.exec_command('version show')
print(stdout.read().decode("utf8"))

print('uploading configupload now....')
#print(upload)


#print(upload)
stdin, stdout, stderr = ssh.exec_command(upload)
print(stdout.read().decode("utf8"))

#close all paramiko open sockets
stdin.close()
stdout.close()
stderr.close()

ssh.close
