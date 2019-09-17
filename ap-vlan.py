#!/usr/bin/env python3

# Requires Python3, TextFSM, Netmiko and PyYAML

import yaml
from netmiko import Netmiko

# import username and password
import creds
username = creds.login['username']
password = creds.login['password']

# definitions
switches = [];

# open the devices doc
with open('devices.yaml', 'r') as f:
    doc = yaml.load(f)

# import a list of devices
for c in doc['switch'].keys():
    switches.append(doc['switch'][c])

for swif in (switches):

    # connect to switch
    myDevice = {
    'host': swif,
    'username': username,
    'password': password,
    'device_type': 'cisco_ios'
    }
    net_connect = Netmiko(**myDevice)
    net_connect.enable()

    lldp = net_connect.send_command("show lldp neighbors detail", use_textfsm=True)

    # iterate over the list
    for lldpf in lldp:

        # grab only "W" capabilities
        if lldpf['capabilities'] == 'W':

            # grab some information
            ap_ip = lldpf['management_ip']
            ap_port = lldpf['local_interface']
            ap_name = lldpf['neighbor']

            # only print if IP is in output
            if "192.168" in ap_ip:
                print (ap_port)
                print (ap_name)
