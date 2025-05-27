path="/root/vdsm/build/RPMS"

cd $path && mkdir vdsm-pkg
cp noarch/vdsm-python-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp x86_64/vdsm-5.50.3.4-1.el8.x86_64.rpm vdsm-pkg/
cp x86_64/vdsm-network-5.50.3.4-1.el8.x86_64.rpm vdsm-pkg/
cp noarch/vdsm-common-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp noarch/vdsm-jsonrpc-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp noarch/vdsm-api-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp noarch/vdsm-client-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp noarch/vdsm-http-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
cp noarch/vdsm-yajsonrpc-5.50.3.4-1.el8.noarch.rpm vdsm-pkg/
tar -czvf vdsm-pkg vdsm-pkg.tar