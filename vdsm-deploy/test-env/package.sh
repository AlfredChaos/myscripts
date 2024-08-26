#!/bin/bash

# 测试环境打包脚本
VDSM_PATH="/root/vdsm/"
VDSM_RPMS_PATH="/root/vdsm/build/RPMS/"


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
    cp ./noarch/vdsm-api-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-client-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-http-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-common-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-jsonrpc-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-python-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./noarch/vdsm-yajsonrpc-5.50.3.4-1.el8.noarch.rpm ./rpms
    cp ./x86_64/vdsm-5.50.3.4-1.el8.x86_64.rpm ./rpms
    cp ./x86_64/vdsm-network-5.50.3.4-1.el8.x86_64.rpm ./rpms
    tar -czvf rpms.tar.gz rpms
}

if [ -d $VDSM_PATH ]; then
    pack
else
    unzip /root/vdsm-20240826.zip
    chmod -R 655 $VDSM_PATH
    pack
fi