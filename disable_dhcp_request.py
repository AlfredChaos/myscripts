import logging
import subprocess


SERVER_PORT=67
CLIENT_PORT=68


def run_command(commands):
    result = subprocess.run(
        commands,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


def execute(commands):
    res, err = run_command(commands)
    if err:
        message = f"execute commands {commands} error = {err}"
        logging.error(message)
    logging.info(f"execute commands {commands} success")
    return res


def get_dhcp_security_rule(southbound, port):
    command_str = "iptables -nvL --line-number | grep " + f"\"{southbound} udp dpt:{port}\" | " + "awk '{print $1}'"

    rule_number = execute([command_str])
    return rule_number


def disable_dhcp_request(southbound):
    if not get_dhcp_security_rule(southbound, SERVER_PORT):
        execute(
            [f"iptables -I FORWARD -m physdev --physdev-in {southbound} -p udp --dport 67 -j DROP"])

    if not get_dhcp_security_rule(southbound, CLIENT_PORT):
        execute(
            [f"iptables -I FORWARD -m physdev --physdev-in {southbound} -p udp --dport 68 -j DROP"])


def enable_dhcp_request(southbound):
    number = get_dhcp_security_rule(southbound, SERVER_PORT)
    if number:
        execute(
            [f"iptables -D FORWARD {number}"])
    number = get_dhcp_security_rule(southbound, CLIENT_PORT)
    if number:
        execute(
            [f"iptables -D FORWARD {number}"])


if __name__ == '__main__':
    southbound = 'bond0.1509'
    enable_dhcp_request(southbound)