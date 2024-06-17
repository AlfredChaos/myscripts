import os
import logging
import psutil
import signal
import shutil

from pyroute2 import netns, IPRoute, NetNS, NSPopen
from file_op import File


DNSMASQ_PATH = "/var/lib/vdsm/dnsmasq"
DNSMASQ_HOSTSFILE = "dnsmasq.hosts.conf"
DNSMASQ_PIDFILE = "dnsmasq.pid"
DNSMASQ_CONF = "dnsmasq.conf"
DNSMASQ_LEASESFILE = "dnsmasq.leases"
DNSMASQ_LOG_PATH = "/var/log/dnsmasq.log"
DNSMASQ_ASYNC_NUM = 50
SERVER_PORT=67
CLIENT_PORT=68


class DhcpServer():
    def __init__(self, id, network, listen_addr, ip_range_start, ip_range_end, 
                 netmask, lease, gateway, nameservers=[]) -> None:
        self.dhcp_namespace = f"dhcp-{id}"
        self.dhcp_server_path = DNSMASQ_PATH + f"/{self.dhcp_namespace}/"
        self.hostsfile_path = os.path.join(self.dhcp_server_path, DNSMASQ_HOSTSFILE)
        self.pidfile_path = os.path.join(self.dhcp_server_path, DNSMASQ_PIDFILE)
        self.dhcp_conf_path = os.path.join(self.dhcp_server_path, DNSMASQ_CONF)
        self.leasefile_path = os.path.join(self.dhcp_server_path, DNSMASQ_LEASESFILE)
        self.main_conf = File(self.dhcp_server_path, DNSMASQ_CONF)
        self.host_file = File(self.dhcp_server_path, DNSMASQ_HOSTSFILE)
        self.pid_file = File(self.dhcp_server_path, DNSMASQ_PIDFILE)
        self.lease_file = File(self.dhcp_server_path, DNSMASQ_LEASESFILE)
        self.network = network
        self.listen_addr = listen_addr
        self.ip_range_start = ip_range_start
        self.ip_range_end = ip_range_end
        self.netmask = netmask
        self.lease = lease
        self.gateway = gateway
        self.nameservers = nameservers
        self.port1 = f"dhcp-{self.dhcp_namespace.split('-')[1]}-1"
        self.port2 = f"dhcp-{self.dhcp_namespace.split('-')[1]}-2"

    def _get_southbound(self):
        pass

    def _is_ns_exist(self):
        for ns in netns.listnetns():
            if self.dhcp_namespace == ns:
                return True
        return False

    def _run(self):
        netns.create(self.dhcp_namespace)
        with IPRoute() as ipr:
            ipr.link('add', ifname=self.port1, kind='veth', peer=self.port2)
            port1_index = ipr.link_lookup(ifname=self.port1)[0]
            port2_index = ipr.link_lookup(ifname=self.port2)[0]
            bridge_index = ipr.link_lookup(ifname=self.network)[0]
            ipr.link('set', index=port1_index, master=bridge_index)
            ipr.link('set', index=port1_index, state='up')
            ipr.link('set', index=port2_index, net_ns_fd=self.dhcp_namespace)
        ns = NetNS(self.dhcp_namespace)
        p2_index = ns.link_lookup(ifname=self.port2)[0]
        ns.link('set', index=p2_index, state='up')
        ns.addr('add', index=p2_index, address=self.listen_addr, mask=24)
        ns.close()
        start_dnsmasq = ['dnsmasq', f'--conf-file={self.dhcp_conf_path}', 
                        f'--pid-file={self.pidfile_path}', 
                        f'--dhcp-hostsfile={self.hostsfile_path}',
                        f'--dhcp-leasefile={self.leasefile_path}']
        NSPopen(self.dhcp_namespace, start_dnsmasq, flags=os.O_CREAT)

    def disable_dhcp_request(self):
        southbound = self._get_southbound()
        dh_namespace = self.dhcp_namespace
        pass 

    def enable_dhcp_request(self):
        dh_namespace = self.dhcp_namespace
        pass

    def update_hostsfile(self, hostsfile):
        if hostsfile:
            self.host_file.clear()
            for hf in hostsfile:
                self.host_file.append(hf)

    def get_dhcp_security_rule(self, port):
        pass

    def disable_dhcp_request(self):
        southbound = self._get_southbound()
        dh_namespace = self.dhcp_namespace
        pass

    def enable_dhcp_request(self):
        dh_namespace = self.dhcp_namespace
        pass

    def update_conf(self, port, dhcp_range, nameservers):
        if not os.path.isfile(self.dhcp_conf_path):
            open(self.dhcp_conf_path, 'w').close()
        self.main_conf.clear()
        content = f'''
no-hosts
no-resolv
strict-order
log-queries
log-facility={DNSMASQ_LOG_PATH}
log-async={DNSMASQ_ASYNC_NUM}
interface={port}
bind-interfaces
listen-address={self.listen_addr}
dhcp-option=option:router,{self.gateway}'''
        self.main_conf.append(content)
        if len(nameservers) != 0:
            dns = ','.join(nameservers)
            content = f"dhcp-option=option:dns-server,{dns}"
            self.main_conf.append(content)
        content = f"dhcp-range={dhcp_range}"
        self.main_conf.append(content)

    def setup(self, hostsfile=None):
        if not os.path.exists(DNSMASQ_PATH):
            os.mkdir(DNSMASQ_PATH)
        if not os.path.exists(self.dhcp_server_path):
            os.mkdir(self.dhcp_server_path)
        self.host_file.create()
        self.pid_file.create()
        self.update_hostsfile(hostsfile)
        dhcp_range = f"{self.ip_range_start},static,{self.netmask},{self.lease}"
        self.update_conf(self.port2, dhcp_range, self.nameservers)
        self._run()
        self.disable_dhcp_request()

    def restart(self):
        target_line = self.main_conf.get_line('listen-address')
        new_line = f"listen-address={self.listen_addr}"
        if target_line:
            self.main_conf.modify(target_line, new_line)
        else:
            self.main_conf.append(new_line)
        self.destroy()
        self._run()
        self.disable_dhcp_request()
        
    def destroy(self, remove_conf_file=False):
        dnsmasq_pid = self.pid_file.read()
        if dnsmasq_pid:
            try:
                psutil.Process(dnsmasq_pid)
                os.kill(dnsmasq_pid, signal.SIGKILL)
            except psutil.NoSuchProcess:
                logging.warning(f"No such process: {dnsmasq_pid}")
            except Exception as e:
                message = f"unable to terminate process: {e}"
                logging.error(message)
                raise message
        if self._is_ns_exist():
            netns.remove(self.dhcp_namespace)
        with IPRoute() as ipr:
            dev_port1 = ipr.link_lookup(ifname=self.port1)
            if len(dev_port1) != 0:
                ipr.link('del', index=dev_port1[0])
            dev_port2 = ipr.link_lookup(ifname=self.port2)
            if len(dev_port2) != 0:
                ipr.link('del', index=dev_port2[0])
        if remove_conf_file:
            shutil.rmtree(self.dhcp_server_path)
        self.enable_dhcp_request()

    def update(self, hostsfile=None):
        dhcp_range = f"{self.ip_range_start},static,{self.netmask},{self.lease}"
        self.update_conf(self.port2, dhcp_range, self.nameservers)
        self.reload()
    
    def get(self):
        dnsmasq_pid = self.pid_file.read()
        if not self._is_ns_exist():
            message = f"dhcp_server {self.dhcp_namespace} not exist"
            logging.error(message)
            raise message
            # raise errors.ConfigNetworkError(errors.ERR_DHCP_SERVER, message)
        try:
            psutil.Process(dnsmasq_pid)
        except psutil.NoSuchProcess:
            message = f"No such process: {dnsmasq_pid}"
            logging.warning(message)
            raise message
            # raise errors.ConfigNetworkError(errors.ERR_DHCP_SERVER, message)
        return dnsmasq_pid
    
    def reload(self):
        dnsmasq_pid = self.pid_file.read()
        try:
            psutil.Process(dnsmasq_pid)
        except psutil.NoSuchProcess:
            logging.warning(f"No such process: {dnsmasq_pid}")
            start_dnsmasq = ['dnsmasq', f'--conf-file={self.dhcp_conf_path}', 
                            f'--pid-file={self.pidfile_path}', 
                            f'--dhcp-hostsfile={self.hostsfile_path}',
                            f'--dhcp-leasefile={self.leasefile_path}']
            NSPopen(self.dhcp_namespace, start_dnsmasq, flags=os.O_CREAT)
            return
        os.kill(dnsmasq_pid, signal.SIGHUP)
    
    def ensure_enable(self):
        try:
            self.get()
        except Exception:
            self.restart()

    def add_host(self, host_info):
        for hinfo in host_info:
            self.host_file.append(hinfo)
        self.reload()

    def remove_host(self, host_info):
        for hinfo in host_info:
            self.host_file.delete_line(hinfo)
            host_mac = hinfo.split(',')[0]
            self.lease_file.delete_line(host_mac)
        self.reload()


                    
