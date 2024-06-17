import os
from pyroute2 import netns, IPRoute, NetNS, NSPopen


namespace = 'test'
port1='p1'
port2='p2'
listen_addr='192.168.1.1'
netns.create(namespace)
network='ovirtmgmt'
with IPRoute() as ipr:
    ipr.link('add', ifname=port1, kind='veth', peer=port2)
    port1_index = ipr.link_lookup(ifname=port1)[0]
    port2_index = ipr.link_lookup(ifname=port2)[0]
    bridge_index = ipr.link_lookup(ifname=network)[0]
    ipr.link('set', index=port1_index, master=bridge_index)
    ipr.link('set', index=port1_index, state='up')
    ipr.link('set', index=port2_index, net_ns_fd=namespace)
ns = NetNS(namespace)
p2_index = ns.link_lookup(ifname=port2)[0]
ns.link('set', index=p2_index, state='up')
ns.addr('add', index=p2_index, address=listen_addr, mask=24)
ns.close()
NSPopen(namespace, ['ip', 'a'], flags=os.O_CREAT)
