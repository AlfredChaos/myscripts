#!/bin/bash

ns=$1
p1=$2
p2=$3
bridge=$4

ip netns add $ns
ip link add $p1 type veth peer name $p2
brctl addif $bridge $p1
ifconfig $p1 up
ip link set $p2 netns $ns
ip netns exec $ns ifconfig $p2 up
ip netns exec $ns dhclient