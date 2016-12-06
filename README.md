# simple_firewall
simple firewall network application working in SDN-enabled OpenFlow-based infrastructure

## Before begin ##
* Install prerequisites: 
  - python-eventlet
  - python-routes
  - python-webob
  - python-paramiko
  - git

* Install Ryu OpenFlow controller. Follow the instructions: https://github.com/osrg/ryu/wiki/OpenFlow_Tutorial

## How to run ##
    ~/ryu/ryu/app$ git clone https://github.com/lukogr/simple_firewall
    ~/ryu$ PYTHONPATH=. ./bin/ryu-manager --verbose ryu/app/simple_firewall/simple_firewall.py
   
## Notes ##
Tested with OpenFlow 1.3 / Ryu 4.8 and Python 2.7

