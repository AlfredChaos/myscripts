#!/bin/bash

HOST_PASSWD=Qjcloud.node@123
HOST_PORT=22

function deploy(){
    sshpass -p $HOST_PASSWD scp -P $HOST_PORT "/root/rpms.tar.gz" root@$1:/root/
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT root@$1 \
    "tar -xzvf /root/rpms.tar.gz && cd /root/rpms/ && rpm -Uvh --nodeps --force *.rpm"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT root@$1 \
    "systemctl restart supervdsmd && systemctl restart vdsmd"
}

for host in "$@"
do
    deploy $host
done