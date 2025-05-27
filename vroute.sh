#!/bin/bash

name=$1
p1=$2
p2=$3
p3=$4
p4=$5
ex_ip=$6
ex_bridge=$7
pri_ip=$8
pri_bridge=$9

ip netns add $name
ip link add $p1 type veth peer name $p2
ip link add $p3 type veth peer name $p4

brctl addif $ex_bridge $p1
ip link set $p2 netns $name
ifconfig $p1 up
ip netns exec $name ifconfig $p2 up
ip netns exec $name ip addr add $ex_ip dev $p2

brctl addif $pri_bridge $p3
ip link set $p4 netns $name
ifconfig $p3 up
ip netns exec $name ifconfig $p4 up
ip netns exec $name ip addr add $pri_ip dev $p4