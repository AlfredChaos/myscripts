#!/bin/bash


VDSM_PATH="/root/vdsm-4.50.3.4/"
VDSM_RPMS_PATH="/root/vdsm-4.50.3.4/build/RPMS/"
HOST_PASSWD=root
HOST_PORT=28822


function pack(){
    for file in `find $VDSM_PATH -type f`
    do
        if file --mime "$file" | grep -iq ': text'; then
            dos2unix "$file"
            echo "Formatted file: $file"
        else
            echo "Skipped non-text file: $file"
        fi
    done
    cd $VDSM_PATH && ./autogen.sh && make && make rpm
    cd $VDSM_RPMS_PATH && mkdir rpms
    cp ./noarch/vdsm-api-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-client-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-http-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-common-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-jsonrpc-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-python-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-yajsonrpc-4.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./x86_64/vdsm-4.50.3.4-1.el8.x86_64.rpm ./rpms
    cp ./x86_64/vdsm-network-4.50.3.4-1.el8.x86_64.rpm ./rpms
    tar -czvf rpms.tar.gz rpms
}


function deploy(){
    sshpass -p $HOST_PASSWD scp -P $HOST_PORT "$VDSM_RPMS_PATH/rpms.tar.gz" root@$1:/root/
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT root@$1 \
    "tar -xzvf /root/rpms.tar.gz && cd /root/rpms/ && rpm -Uvh --nodeps --force *.rpm"
    sshpass -p $HOST_PASSWD ssh -p $HOST_PORT root@$1 \
    "systemctl restart supervdsmd && systemctl restart vdsmd"
}


if [ -d $VDSM_PATH ]; then
    pack
else
    if [ -d "/root/vdsm/" ]; then
        mv /root/vdsm $VDSM_PATH
        pack
    else
        echo "Cannot find the code"
        exit
    fi
fi


for host in "$@"
do
    deploy $host
done