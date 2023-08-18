import os
import shutil
import subprocess

DNSMASQ_PATH = "/var/lib/vdsm/dnsmasq"
DNSMASQ_HOSTFILE = "dnsmasq.hostfile"
DNSMASQ_PIDFILE = "dnsmasq.pid"


def run_command(commands):
    result = subprocess.run(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


def execute(commands):
    res, err = run_command(commands)
    if err:
        print(f"###Execute Commands {commands} Error = {err}")
        raise
    print(f"+++Execute Commands {commands} success = {res}")
    return res


def update_hostfile(hostfile_path, hostfile=None):
    if hostfile:
        execute(["echo", "", ">", f"{hostfile_path}"])
        for hf in hostfile:
            hostfile_content = f"dhcp-host={hf}"
            execute(["echo", f"{hostfile_content}", ">>", f"{hostfile_path}"])


def setup_dhcp_server(bridge, network_id, listen_addr, ip_range_start, 
                      ip_range_end, netmask, lease, hostfile=None):
    if not os.path.exists(DNSMASQ_PATH):
        os.mkdir(DNSMASQ_PATH)
    dhcp_namespace = f"dhcp-{network_id}"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    if not os.path.exists(dhcp_server_path):
        os.mkdir(dhcp_server_path)
    hostfile_path = os.path.join(dhcp_server_path, DNSMASQ_HOSTFILE)
    if not os.path.isfile(hostfile_path):
        open(hostfile_path, 'w').close()
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    if not os.path.isfile(pidfile_path):
        open(pidfile_path, 'w').close()
    update_hostfile(hostfile_path, hostfile)
    port1 = f"{dhcp_namespace}-1"
    port2 = f"{dhcp_namespace}-2"
    dhcp_range = f"{ip_range_start},{ip_range_end},{netmask},{lease}"
    execute(["sudo", "ip", "netns", "add", f"{dhcp_namespace}"])
    execute(["sudo", "ip", "link", "add", f"{port1}", "type", "veth", "peer", "name", f"{port2}"])
    execute(["sudo", "ip", "link", "set", "dev", f"{port1}", "master", f"{bridge}"])
    execute(["sudo", "ip", "link", "set", "dev", f"{port1}", "up"])
    execute(["sudo", "ip", "link", "set", f"{port2}", "netns", f"{dhcp_namespace}"])
    execute(["sudo", "ip", "netns", "exec", f"{dhcp_namespace}", "ip", "link", "set", f"{port2}", "up"])
    execute(["sudo", "ip", "netns", "exec", f"{dhcp_namespace}", "ip", "addr", "add", f"{listen_addr}", "dev", f"{port2}"])
    execute(["sudo", "ip", "netns", "exec", f"{dhcp_namespace}", "dnsmasq", "--no-hosts", 
             "--no-resolv", "--strict-order", "--bind-interfaces", f"--interface={port2}", 
             f"--pid-file={pidfile_path}", f"--dhcp-hostfile={hostfile_path}", 
             f"--dhcp-range={dhcp_range}"])
    

def destroy_dhcp_server(network_id):
    dhcp_namespace = f"dhcp-{network_id}"
    port2 = f"{dhcp_namespace}-2"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    dnsmasq_pid = execute(["sudo", "cat", f"{pidfile_path}"])
    execute(["sudo", "kill", f"{dnsmasq_pid}"])
    execute(["sudo", "ip", "netns", "del", f"{dhcp_namespace}"])
    execute(["sudo", "ip", "link", "set", f"{port2}", "nomaster"])
    execute(["sudo", "ip", "link", "delete", f"{port2}"])
    shutil.rmtree(dhcp_server_path)


def update_dhcp_server(network_id, ip_range_start, 
                      ip_range_end, netmask, lease, hostfile=None):
    dhcp_namespace = f"dhcp-{network_id}"
    port2 = f"{dhcp_namespace}-2"
    dhcp_server_path = DNSMASQ_PATH + f"/{dhcp_namespace}/"
    hostfile_path = os.path.join(dhcp_server_path, DNSMASQ_HOSTFILE)
    pidfile_path = os.path.join(dhcp_server_path, DNSMASQ_PIDFILE)
    dnsmasq_pid = execute(["sudo", "cat", f"{pidfile_path}"])
    dhcp_range = f"{ip_range_start},{ip_range_end},{netmask},{lease}"
    update_hostfile(hostfile_path, hostfile)
    execute(["sudo", "kill", f"{dnsmasq_pid}"])
    execute(["sudo", "ip", "netns", "exec", f"{dhcp_namespace}", "dnsmasq", "--no-hosts", 
             "--no-resolv", "--strict-order", "--bind-interfaces", f"--interface={port2}", 
             f"--pid-file={pidfile_path}", f"--dhcp-hostfile={hostfile_path}", 
             f"--dhcp-range={dhcp_range}"])
