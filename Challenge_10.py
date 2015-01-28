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
server_dict={}
nodes = ""

#Setup variables
build_num = 2
build_name = 'denz7201_CH10_'

# define functions

def build_server(serv_name):
  return cs.servers.create(serv_name, my_img.id, my_flavor.id)

def get_server_data(server_name):
  print "Retrieving",server_name ,"Information"
  print "Please Wait"
  server_obj = server_dict[server_name]
  resultz = pyrax.utils.wait_until(serv_obj, "status", ["ACTIVE", "ERROR"])
  print "Admin password:", server_obj.adminPass
  print "Networks:", server_obj.networks
  return ()

# Pick an image Function
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

# Pick a Flavor Function
def get_flavor_obj(Instance, ram_select):
  my_flavor = [flavor for flavor in cs.flavors.list()
  if str(Instance) in flavor.human_id
  and flavor.ram == ram_select][0]
  return (my_flavor)

# Build Server Wrapper Function
def build_one():
  for this_one in range (1, build_num + 1):
    serv_name = build_name + str(this_one)
    serv_obj = build_server (serv_name)
    server_dict[serv_name] = serv_obj
  return ()
# check the server status and wait for it until it is ready
def check_ready():
  for this_one in range (1, build_num + 1):
    server_name = build_name + str(this_one)
    server_obj = server_dict[server_name]
    print server_obj
    resultz = pyrax.utils.wait_until(server_obj, "status", ["ACTIVE", "ERROR"])
  return(resultz)
# main

my_img = get_image_obj("Ubuntu 14", 1)
my_flavor = get_flavor_obj("standard", 512)
build_one()
resultz = check_ready()
# Get the private network IPs for the servers create a node and setup the lb
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create("denz7201_ch10_lb", port=80, protocol="HTTP", nodes=[], virtual_ips=[vip])
resultz = pyrax.utils.wait_until(lb, "status", ["ACTIVE", "ERROR"])
for this_one in range (1, build_num + 1):
  this_server = build_name + str(this_one)
  server_obj = server_dict[this_server]
  this_server_ip = server_obj.networks["private"][0]
  this_node = clb.Node(address=this_server_ip, port=80, condition="ENABLED")
  resultz = pyrax.utils.wait_until(lb, "status", ["ACTIVE", "ERROR"])
  lb.add_nodes([this_node])
html = "<html><body>Sorry, something is amiss!</body></html>"
lb.set_error_page(html)




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
