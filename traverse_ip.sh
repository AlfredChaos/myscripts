#!/bin/bash

# 起始IP地址
start_ip="192.168.1.21"
# 结束IP地址
end_ip="192.168.1.30"

# 将IP地址转换为整数的函数
function get_ip_int() {
   IFS='.' read -ra ip_parts <<< "$1"
   ip_int=$(( ${ip_parts[0]}*256*256*256 + ${ip_parts[1]}*256*256 + ${ip_parts[2]}*256 + ${ip_parts[3]} ))
   echo $ip_int
}

# 将整数转换回IP地址的函数
function int_to_ip() {
   ip_int=$1
   echo $((ip_int>>24)).$(( (ip_int>>16)&255 )).$(( (ip_int>>8)&255 )).$(( ip_int&255 ))
}

# 将IP地址转换为整数
start_ip_int=$(get_ip_int "$start_ip")
end_ip_int=$(get_ip_int "$end_ip")

# 遍历IP地址
for (( ip_int=start_ip_int; ip_int<=end_ip_int; ip_int++ )); do
    # 将整数转换回IP地址
    ip=$(int_to_ip "$ip_int")
    echo "$ip"
done