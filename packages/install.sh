#!/bin/bash

node_ip=$1

root_path=/root
path=${root_path}/alfred
node_pass=Qjcloud.node@123

echo "#####################"
echo "send to node ${node_ip}"
sshpass -p ${node_pass} -o StrictHostChecking=no scp ${path}/packages.tar root@${node_ip}:/root
echo "sent complete"

echo "#####################"
echo "node ${node_ip} installing..."
sshpass -p ${node_pass} -o StrictHostChecking=no ssh root@${node_ip} "tar -xzvf /root/packages.tar"
sshpass -p ${node_pass} -o StrictHostChecking=no ssh root@${node_ip} "cd /root/packages & rpm -Uvh --nodeps --force *.rpm"
sshpass -p ${node_pass} -o StrictHostChecking=no ssh root@${node_ip} "systemctl restart supervdsmd"
sshpass -p ${node_pass} -o StrictHostChecking=no ssh root@${node_ip} "systemctl restart vdsmd"
echo "node ${node_ip} install complete"