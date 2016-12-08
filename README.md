# simple_firewall
simple_firewall is a network application dedicated for the SDN-enabled OpenFlow-based infrastructure. It runs with [Ryu] (https://osrg.github.io/ryu/) OpenFlow controller.

simple_firewall application allows to 
  - set user-defined security rules for ICMP, UDP and TCP network traffic 
  - monitor unwanted flows
It is based on the rest_firewall Ryu example application, but it implements also the forwarding engine to forward IP packets based on static routing table. Moreover it learns MAC adresses on ports to avoid ARP flooding each time.

## Before begin ##
* Install prerequisites: 
  - python-eventlet
  - python-routes
  - python-webob
  - python-paramiko
  - git
  
On ubuntu:

    $sudo apt-get install python-eventlet python-routes python-webob python-paramiko git

* Install Ryu OpenFlow controller. You may follow the instructions from the [tutorial] (https://github.com/osrg/ryu/wiki/OpenFlow_Tutorial).

## How to run ##
### Get last code from GitHub ###

    ~/ryu/ryu/app$ git clone https://github.com/lukogr/simple_firewall

### Configure static network routing ###
Edit simple_firewall_conf.py and change topology_conf.
All static routing entries for every OF switch should be configured before running the application. DPID (data path ID) may be retrieved from the command line of the switch.
topology_conf has the following structure:
    
    topology_conf= {

        hex_OpenFlow_switch_DPID:
        {
            "dst_subnet/mask": out_port 
        }
    }

Example topology_conf:

    topology_conf = {

        0x000000223d5a0019:
        {
            "192.168.0.1/24": 8,
            "192.168.20.2/24": 6
        },    

        0x5e3e486e730002fe:
        {
            "192.168.0.1/24": 45,
            "192.168.20.2/24": 46
        },

    }

### Configure firewall rules in the file ###
By default simple_firewall blocks all traffic on the switch. Application monitors and displays not-ALLOWED flows.

All rules set in the simple_firewall_conf.py file are automaticaly applied by the simple_firewall application just after OpenFlow switch connects to the controller (only once). In case of any change in the configuration, application should be restarted.

Example configuration (to change) allow bidirectional ICMP traffic (ping) between 192.168.0.0 and 192.168.20.0 subnets:

    firewall_rules = [
        {
            "priority":"100",
            "nw_src":"192.168.20.2/24",
            "nw_dst":"192.168.0.1/24",
            "nw_proto":"ICMP",
            "actions":"ALLOW"
        },
        {
            "priority":"100",
            "nw_src":"192.168.0.1/24",
            "nw_dst":"192.168.20.2/24",
            "nw_proto":"ICMP",
            "actions":"ALLOW"
        },    
    ]

### Run simple_firewall as Ryu application ###

    ~/ryu$ PYTHONPATH=. ./bin/ryu-manager --verbose ryu/app/simple_firewall/simple_firewall.py

## REST API of the application ##
simple_firewall exposes API (defined also in rest_firewall app) through http://{service_IP_address}:8080 which allows to add/delete firewall rules during runtime.

    # =============================
    #          REST API
    # =============================
    #
    #  Note: specify switch and vlan group, as follows.
    #   {switch-id} : 'all' or switchID
    #   {vlan-id}   : 'all' or vlanID
    #
    #

    # about Firewall status
    #
    # get status of all firewall switches
    # GET /firewall/module/status
    #
    # set enable the firewall switches
    # PUT /firewall/module/enable/{switch-id}
    #
    # set disable the firewall switches
    # PUT /firewall/module/disable/{switch-id}
    #

    # about Firewall logs
    #
    # get log status of all firewall switches
    # GET /firewall/log/status
    #
    # set log enable the firewall switches
    # PUT /firewall/log/enable/{switch-id}
    #
    # set log disable the firewall switches
    # PUT /firewall/log/disable/{switch-id}
    #

    # about Firewall rules
    #
    # get rules of the firewall switches
    # * for no vlan
    # GET /firewall/rules/{switch-id}
    #
    # * for specific vlan group
    # GET /firewall/rules/{switch-id}/{vlan-id}
    #
    #
    # set a rule to the firewall switches
    # * for no vlan
    # POST /firewall/rules/{switch-id}
    #
    # * for specific vlan group
    # POST /firewall/rules/{switch-id}/{vlan-id}
    #
    #  request body format:
    #   {"<field1>":"<value1>", "<field2>":"<value2>",...}
    #
    #     <field>  : <value>
    #    "priority": "0 to 65533"
    #    "in_port" : "<int>"
    #    "dl_src"  : "<xx:xx:xx:xx:xx:xx>"
    #    "dl_dst"  : "<xx:xx:xx:xx:xx:xx>"
    #    "dl_type" : "<ARP or IPv4 or IPv6>"
    #    "nw_src"  : "<A.B.C.D/M>"
    #    "nw_dst"  : "<A.B.C.D/M>"
    #    "ipv6_src": "<xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/M>"
    #    "ipv6_dst": "<xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/M>"
    #    "nw_proto": "<TCP or UDP or ICMP or ICMPv6>"
    #    "tp_src"  : "<int>"
    #    "tp_dst"  : "<int>"
    #    "actions" : "<ALLOW or DENY>"
    #
    #   Note: specifying nw_src/nw_dst
    #         without specifying dl-type as "ARP" or "IPv4"
    #         will automatically set dl-type as "IPv4".
    #
    #   Note: specifying ipv6_src/ipv6_dst
    #         without specifying dl-type as "IPv6"
    #         will automatically set dl-type as "IPv6".
    #
    #   Note: When "priority" has not been set up,
    #         "0" is set to "priority".
    #
    #   Note: When "actions" has not been set up,
    #         "ALLOW" is set to "actions".
    #
    #
    # delete a rule of the firewall switches from ruleID
    # * for no vlan
    # DELETE /firewall/rules/{switch-id}
    #
    # * for specific vlan group
    # DELETE /firewall/rules/{switch-id}/{vlan-id}
    #
    #  request body format:
    #   {"<field>":"<value>"}
    #
    #     <field>  : <value>
    #    "rule_id" : "<int>" or "all"
    #
    #--------------------------------------------------------------------

   
## Notes ##
Tested with OpenFlow 1.3 [Pica8-3822 and NoviFlow-2128 switches] / Ryu 4.8 and Python 2.7
OS: ubuntu14.04
