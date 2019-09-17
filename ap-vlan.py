#!/usr/bin/env python3

# Requires Python3, TextFSM, Netmiko and PyYAML

import yaml
from netmiko import Netmiko

# import username and password
import creds
username = creds.login['username']
password = creds.login['password']

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

    shvlan = net_connect.send_command("show lldp neighbors", use_textfsm=True)

    # iterate over the list and grab the dict with intf
    for i in shvlan:
        if i['port'] == intf:
            # grab VLAN from dict
            vlan = i['vlan']
