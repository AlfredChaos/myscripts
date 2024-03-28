#!/usr/bin/python3

# params = {
#     'dirction': ['egress', 'ingress'],
#     'protocol': '',
#     'ethertype': ['ipv4', 'ipv6'],
#     'port_range_max': 0,
#     'port_range_min': 0,
#     'remote_ip_prefix': '10.0.0.0/24',
#     'action': ['Accept', 'Drop']
# }

import subprocess


Directions = ['egress', 'ingress']
Protocls = {
    '0': 'any',
    '51': 'ah',
    '33': 'dccp',
    '1': 'icmp',
    '2': 'igmp',
    '4': 'ipip',
    '6': 'tcp',
    '17': 'udp',
    '112': 'vrrp'
}
Ethertypes = ['ipv4']
Actions = ['ACCEPT', 'DROP']

def execute(cmd):
    result = subprocess.run()

def generate(params):
    cmd = ['iptables -A']
    direction = params.get('direction')
    if direction not in Directions:
        print('unsupport direction')
        return
    if direction == 'egress':
        direction = 'OUTPUT'
    else:
        direction = 'INPUT'
    cmd.append(direction)

    protocol = params.get('direction', '0')
    pro_numbers = []
    pro_names = []
    for key, value in Protocls.items():
        pro_numbers.append(key)
        pro_names.append(value)
    if protocol not in pro_names and protocol not in pro_numbers:
        print("unsupport protocol")
        return
    cmd.append(f'-p {protocol}')

    ethertype = params.get('ethertype', 'ipv4')
    if ethertype not in Ethertypes:
        print("unsupport ethertype")
        return
    
    port_range_max = params.get('port_range_max', 65535)
    if port_range_max < 0 or port_range_max > 65535:
        print("unsupport port")
        return
    port_range_min = params.get('port_range_min', 0)
    if port_range_min < 0 or port_range_min > 65535:
        print("unsupport port")
        return
    remote_ip_prefix = params.get('remote_ip_prefix', '0.0.0.0/0')
    action = params.get('action')
    if action not in Actions:
        print("unsupport action")
        return
    
    base_cmd = 'iptables'


def main():
    pass

if __name__ == '__main__':
    main()