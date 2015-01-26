#!/usr/bin/env python

import os
import sys
import time
import pyrax
from os.path import expanduser
from pprint import pprint

# account info
home = expanduser("~")
pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials.current")
pyrax.set_credential_file(creds_file)

# Setup pyrax
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns
cf = pyrax.cloudfiles


# define functions

def build_server(serv_name, my_img_id, flavor_512_id):
  return cs.servers.create(serv_name, my_img_id, flavor_512_id)

def get_server_data(server_name):
  print "Retrieving",server_name ,"Information"
  print "Please Wait"
  server_obj = server_dict[server_name]
  resultz = pyrax.utils.wait_until(serv_obj, "status", ["ACTIVE", "ERROR"])
  print "Admin password:", server_obj.adminPass
  print "Networks:", server_obj.networks
  return ()

def get_image_obj(OS_name, PVHVM_bool):
  if PVHVM_bool :
    my_img = [img for img in cs.images.list()
    if str(OS_name) in img.name
    and "PVHVM" in img.name][0]
  else:
    my_img = [img for img in cs.images.list()
    if str(OS_name) in img.name
    and "PVHVM" not in img.name][0]
  return (my_img)

def get_flavor_obj(Instance, ram_select):
  my_flavor = [flavor for flavor in cs.flavors.list()
  if str(Instance) in flavor.human_id
  and flavor.ram == ram_select][0]
  return (my_flavor)
  
  
  # Get the private network IPs for the servers
server1_ip = server1.networks["private"][0]
server2_ip = server2.networks["private"][0]

# Use the IPs to create the nodes
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

lb = clb.create("example_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])




'''
Challenge 10

Write an application that will:

    Create 2 servers, supplying an ssh key to be installed at /root/.ssh/authorized_keys.
    Create a load balancer
    Add the 2 new servers to the LB
    Set up LB monitor and custom error page.
    Create a DNS record based on a FQDN for the LB VIP.
    Write the error page html to a file in cloud files for backup.

Whew! That one is worth 8 points!
'''