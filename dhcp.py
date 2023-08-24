import os
import sys
import shutil
import subprocess

DNSMASQ_PATH = "/var/lib/vdsm/dnsmasq"
DNSMASQ_HOSTSFILE = "dnsmasq.hosts.conf"
DNSMASQ_PIDFILE = "dnsmasq.pid"

action = sys.argv[1]


def run_command(commands):
    result = subprocess.run(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


def execute(commands):
    res, err = run_command(commands)
    if err:
        print(f"###Execute Commands {commands} Error = {err}")
        raise
    print(f"+++Execute Commands {commands} success")
    return res


def update_hostsfile(hostsfile_path, hostsfile=None):
    if hostsfile:
        execute([f"> {hostsfile_path}"])
        for hf in hostsfile:
            execute([f"echo {hf} >> {hostsfile_path}"])


def setup_dhcp_server(bridge, dhcp_id, listen_addr, ip_range_start, 
                      ip_range_end, netmask, lease, hostsfile=None):
    if not os.path.exists(DNSMASQ_PATH):
        os.mkdir(DNSMASQ_PATH)
    dhcp_namespace = f"dhcp-{dhcp_id}"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    if not os.path.exists(dhcp_server_path):
        os.mkdir(dhcp_server_path)
    hostsfile_path = os.path.join(dhcp_server_path, DNSMASQ_HOSTSFILE)
    if not os.path.isfile(hostsfile_path):
        open(hostsfile_path, 'w').close()
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    if not os.path.isfile(pidfile_path):
        open(pidfile_path, 'w').close()
    update_hostsfile(hostsfile_path, hostsfile)
    port1 = f"dhcp-{dhcp_namespace.split('-')[1]}-1"
    port2 = f"dhcp-{dhcp_namespace.split('-')[1]}-2"
    dhcp_range = f"{ip_range_start},{ip_range_end},{netmask},{lease}"
    execute([f"sudo ip netns add {dhcp_namespace}"])
    execute([f"sudo ip link add {port1} type veth peer name {port2}"])
    execute([f"sudo ip link set dev {port1} master {bridge}"])
    execute([f"sudo ip link set dev {port1} up"])
    execute([f"sudo ip link set {port2} netns {dhcp_namespace}"])
    execute([f"sudo ip netns exec {dhcp_namespace} ip link set {port2} up"])
    execute([f"sudo ip netns exec {dhcp_namespace} ip addr add {listen_addr} dev {port2}"])
    execute([f"sudo ip netns exec {dhcp_namespace} dnsmasq --no-hosts --no-resolv --strict-order \
             --bind-interfaces --interface={port2} --pid-file={pidfile_path} --dhcp-hostsfile={hostsfile_path} \
             --dhcp-range={dhcp_range}"])
    

def destroy_dhcp_server(dhcp_id):
    dhcp_namespace = f"dhcp-{dhcp_id}"
    port2 = f"dhcp-{dhcp_namespace.split('-')[1]}-2"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    dnsmasq_pid = execute([f"sudo cat {pidfile_path}"])
    execute([f"sudo kill {dnsmasq_pid}"])
    execute([f"sudo ip netns del {dhcp_namespace}"])
    res, err = run_command([f"sudo ip link show {port2}"])
    print(f'======res = {res}')
    print(f'======err = {err}')
    if not err:
        execute([f"sudo ip link set {port2} nomaster"])
        execute([f"sudo ip link delete {port2}"])
    shutil.rmtree(dhcp_server_path)


def update_dhcp_server(dhcp_id, ip_range_start, 
                      ip_range_end, netmask, lease, hostsfile=None):
    dhcp_namespace = f"dhcp-{dhcp_id}"
    port2 = f"dhcp-{dhcp_namespace.split('-')[1]}-2"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    hostsfile_path = os.path.join(dhcp_server_path, DNSMASQ_HOSTSFILE)
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    dnsmasq_pid = execute([f"sudo cat {pidfile_path}"])
    dhcp_range = f"{ip_range_start},{ip_range_end},{netmask},{lease}"
    update_hostsfile(hostsfile_path, hostsfile)
    execute([f"sudo kill {dnsmasq_pid}"])
    execute([f"sudo ip netns exec {dhcp_namespace} dnsmasq --no-hosts --no-resolv \
             --strict-order --bind-interfaces --interface={port2} --pid-file={pidfile_path} \
             --dhcp-hostsfile={hostsfile_path} --dhcp-range={dhcp_range}"])


bridge = 'mybridge'
dhcp_id = '6ba7b810-9dad-11d1-80b4-00c04fd430c8'
listen_addr = '192.168.1.2/24'
ip_range_start = '192.168.1.3'
ip_range_end = '192.168.1.254'
netmask = '255.255.255.0'
lease = '24h'
hostsfile = ['42:d9:12:b5:ba:e0,192.168.1.226']

if __name__ == '__main__':
    if action == 'setup':
        setup_dhcp_server(bridge, dhcp_id, listen_addr, ip_range_start,
                          ip_range_end, netmask, lease)
    elif action == 'update':
        update_dhcp_server(dhcp_id, ip_range_start, ip_range_end,
                           netmask, lease, hostsfile)
    elif action == 'destroy':
        destroy_dhcp_server(dhcp_id)
    else:
        print(f'###Action {action} not support')