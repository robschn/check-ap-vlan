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

# iterate over switches to connect
for swif in (switches):

    # connect to switch
    print ("\nConnecting to " +swif+ " now...")
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

            # only print if IP is not in output
            if "172.22." not in ap_ip:
                print ("\nFound " +ap_name+ " on port " +ap_port+ "..")

                # find and grab AP VLAN
                status = net_connect.send_command("show interface status", use_textfsm=True)
                for statusf in status:
                    if statusf['port'] == ap_port:
                        ap_vlan = statusf['vlan']

                        # seperate the vlan into digits
                        split_vlan = list(str(ap_vlan))
                        # first digit of the vlan
                        net_vlan = split_vlan[0]
                        # combine first digit with 2
                        new_vlan = net_vlan+ "2"

                        # send commands
                        print ("Changing VLAN from " +ap_vlan+ " to " +new_vlan+ "..")
                        config_commands = [
                        'int '+ap_port,
                        'shut'
                        'desc ' +ap_name,
                        'swi acc vlan '+new_vlan,
                        'no shut'
                        ]

                        net_connect.send_config_set(config_commands)
                        print ("\nDone!")
