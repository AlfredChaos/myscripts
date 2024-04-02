#!/bin/bash

name=$1  # vroute name
p1=$2   # vroute对外接口p1
p2=$3   # vroute对外接口p2
p3=$4   # vroute对内接口p1
p4=$5   # vroute对内接口p2
ex_ip=$6    # vroute外网ip
ex_bridge=$7    # vroute外接网桥
pri_ip=$8   # vroute内网网关ip
pri_bridge=$9   # vroute内接网桥
vm=${10}    # 虚拟机名字
vm_port1=${11}  # 虚拟机接口p1
vm_port2=${12}  # 虚拟机接口p2
vm_ip=${13}     # 虚拟机内部ip
ex_gw=${14}     # 外网网关
pri_net=${15}   # 内网网段
snat_ip=${16}   # 虚拟机出外网的ip


# 创建vroute、vm
ip netns add $name
ip netns add $vm
ip link add $p1 type veth peer name $p2
ip link add $p3 type veth peer name $p4
ip link add $vm_port1 type veth peer name $vm_port2

# vroute绑定外部网络
brctl addif $ex_bridge $p1
ip link set $p2 netns $name
ifconfig $p1 up
ip netns exec $name ifconfig $p2 up
ip netns exec $name ip addr add $ex_ip dev $p2

# vroute绑定内网
brctl addif $pri_bridge $p3
ip link set $p4 netns $name
ifconfig $p3 up
ip netns exec $name ifconfig $p4 up
ip netns exec $name ip addr add $pri_ip dev $p4

# vm绑定内网
brctl addif $pri_bridge $vm_port1
ip link set $vm_port2 netns $vm
ifconfig $vm_port1 up
ip netns exec $vm ifconfig $vm_port2 up
ip netns exec $vm ip addr add $vm_ip dev $vm_port2

# 添加默认路由
ip netns exec $vm ip route add default via $pri_ip
ip netns exec $name ip route add default via $ex_gw

# 检查环境
ip netns exec $name sysctl -w net.ipv4.ip_forward=1

# 添加snat
ip netns exec $name iptables -t nat -A POSTROUTING -s $pri_net -j SNAT --to-source $snat_ip

