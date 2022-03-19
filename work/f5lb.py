#!/usr/bin/python3

import sys
import paramiko
import datetime
import time
from paramiko import SSHClient, AutoAddPolicy
from paramiko import client

# declare hostnames (ensure DNS updated).temp use IP
# pwd have been delegated to arguments as argv[4] and ansible vaulted
f5lb_host = 'DC3-LB1-INT.dc.mgmt'
f5lb_usr = 'irwan'
#f5lb_pwd = 'G00dwi11!234()'



# full command: tcpdump -ni 0.0 -W 10 -C 100 -w /var/tmp/test.pcap host <host_ip> and port <port_no>
# -c is size, -W  is no of logs rotating
# parsing as arguments to make script ansible friendly
print ("This is the name of the script: ",sys.argv[0])
print ("To run script: ./f5lb_arg.py <f5_interface> <host_ip> <host_port> <f5lb_pwd>")

f5lb_int = sys.argv[1]
host_ip = sys.argv[2]
host_port = sys.argv[3]
f5lb_pwd = sys.argv[4]

# declare variables
now = datetime.datetime.now()
log_time = now.strftime("%Y%m%d%s")
out_path = "/var/tmp/"                                                                                                                                                                                                                                                                 
out_file = host_ip + "_" + host_port + "_" + log_time  + ".pcap"
out_w = out_path + out_file

# start the script
print("Script executed at", log_time)

# command: tcpdump -ni 1.1 -W 3 -C 1 -w %s host 202.55.76.114 and port 443
start_tcpdump = 'tcpdump -ni %s -W 3 -C 1 -w %s host %s and port %s &' % (f5lb_int, out_w, host_ip, host_port)

# ssh to f5lb switch
# added allow_agent=false to remove ssh error -20211226
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

#print('ssh.connect', f5lb_host, f5lb_usr, f5lb_pwd )
try:
    ssh.connect(f5lb_host, username=f5lb_usr, password=f5lb_pwd, allow_agent=False)

    print('Print Interfaces:....')
    stdin, stdout, stderr = ssh.exec_command('show net interface')
    print(stdout.read().decode("utf8"))

    # to allow background tcpdump run...
    print('Switching to bash')
    term = ssh.invoke_shell()
    term.send('bash\n')
    time.sleep(2)
    term.send('echo "$SHELL"\n')
    term_out = term.recv(65535).decode("utf-8")
    print(term_out)  
    time.sleep(2)
    print(term_out) 
    

    print('Now run tcpdump in the bash shell...\n')
    term.send(start_tcpdump)
    time.sleep(2)
    term.send('\n')
    time.sleep(2)
    term.send('\n')
    time.sleep(2)

    print('check the output of ps')
    term.send('ps -ef | grep -i tcp\n')
    time.sleep(2)
    term_out = term.recv(65535).decode("utf-8")
    print(str(term_out) + "\n")


    #close all paramiko open sockets
    stdin.close()
    stdout.close()
    stderr.close()
    #stdin, stdout, stderr = ssh.close

    ssh.close()

except paramiko.AuthenticationException:
    print ("Incorrect password: "+f5lb_pwd)

except socket.erro:
    print ("Socket Error")

except:
    print("Something Went Wrong")

