topology_conf = {
    
    #hex_OpenFlow_switch_DPID:
    #{
    #    "dst_subnet": out_port       
    #}
    
    # NoviSwitch
    0x000000223d5a0019:
    {
        "192.168.0.1/24": 8,
        "192.168.20.2/24": 6
    },    

    #Pica8
    0x5e3e486e730002fe:
    {
        "192.168.0.1/24": 45,
        "192.168.20.2/24": 46
    },
 
}
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
    

 

