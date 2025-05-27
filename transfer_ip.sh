#!/bin/bash

# 起始IP地址
start_ip="10.127.72.51"
# 结束IP地址
end_ip="10.127.72.60"
HOST_PASSWD=Qjcloud.node@123
HOST_PORT=22

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

function deploy(){
    sshpass -p $HOST_PASSWD scp -P $HOST_PORT -o "StrictHostKeyChecking no" "/root/alfred/python-dist.zip" root@$1:/root/
    sshpass -p $HOST_PASSWD scp -P $HOST_PORT -o "StrictHostKeyChecking no" "/root/alfred/rpms.tar.gz" root@$1:/root/
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT -o StrictHostKeyChecking=no root@$1 \
    "unzip /root/python-dist.zip -d /opt/raystack-packages"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT -o StrictHostKeyChecking=no root@$1 \
    "rpm -i /opt/raystack-packages/python3-psutil-5.7.3-1.el8.x86_64.rpm"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT -o StrictHostKeyChecking=no root@$1 \
    "pip3 install --no-index --find-links=/opt/raystack-packages/python-dist/pyroute2 pyroute2"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT -o StrictHostKeyChecking=no root@$1 \
    "tar -xzvf /root/rpms.tar.gz && cd /root/rpms/ && rpm -Uvh --nodeps --force *.rpm"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT -o StrictHostKeyChecking=no root@$1 \
    "systemctl restart supervdsmd && systemctl restart vdsmd"
}

# 将IP地址转换为整数
start_ip_int=$(get_ip_int "$start_ip")
end_ip_int=$(get_ip_int "$end_ip")

# 遍历IP地址
for (( ip_int=start_ip_int; ip_int<=end_ip_int; ip_int++ )); do
    # 将整数转换回IP地址
    ip=$(int_to_ip "$ip_int")
    echo ""
    echo "++++++++++++Current Update $ip+++++++++++++++++++++"
    deploy "$ip"
done