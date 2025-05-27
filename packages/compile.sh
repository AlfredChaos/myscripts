#!/bin/bash

root_path=/root
path=${root_path}/vdsm
mgmt_ip=10.123.10.199
mgmt_pass=Qjcloud.com@123
mgmt_port=4444


echo "########################"
echo "start compiling..."
cd ${path}
git checkout master
git pull
./autogen.sh
make
make rpm

cd ${path}/build/RPMS/
mkdir packages
cp noarch/vdsm-jsonrpc-4.50.3.4-1.el8.noarch.rpm ./packages
cp x86_64/vdsm-network-4.50.3.4-1.el8.x86_64.rpm ./packages
cp noarch/vdsm-api-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-python-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-client-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-yajsonrpc-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-http-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-common-4.50.3.4-1.el8.noarch.rpm ./packages
cp noarch/vdsm-jsonrpc-4.50.3.4-1.el8.noarch.rpm ./packages
cp x86_64/vdsm-4.50.3.4-1.el8.x86_64.rpm ./packages
tar -czvf packages.tar packages
echo "compile complete"

echo "#############################"
echo "send to mgmt"
sshpass -p ${mgmt_pass} -o StrictHostChecking=no scp packages.tar root@${mgmt_ip}:/root/alfred/ -P ${mgmt_port}
for ip in "$@"; do
    sshpass -p ${mgmt_pass} -o StrictHostChecking=no ssh root@${mgmt_ip} "bash /root/alfred/install.sh ${ip}"
done
echo "sent complete"
