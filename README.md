# simple_firewall
simple firewall network application working in SDN-enabled OpenFlow-based infrastructure

## How to run ##
    ~/ryu/ryu/app$ git clone https://github.com/lukogr/simple_firewall
    ~/ryu$ PYTHONPATH=. ./bin/ryu-manager --verbose ryu/app/simple_firewall/simple_firewall.py
   
## Notes ##
Tested with OpenFlow 1.3 and Ryu 4.8

