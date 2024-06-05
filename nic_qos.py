#!/usr/bin/python3

import hooking


def set_interface_qos(domxml):
    for iface in domxml.getElementsByTagName('interface'):
        bandwidth_node = domxml.createElement('bandwidth')

        inbound_node = domxml.createElement('inbound')
        inbound_node.setAttribute('average', '2048')
        bandwidth_node.appendChild(inbound_node)

        outbound_node = domxml.createElement('outbound')
        outbound_node.setAttribute('average', '2048')
        bandwidth_node.appendChild(outbound_node)

        iface.appendChild(bandwidth_node)


def main():
    domxml = hooking.read_domxml()
    try:
        set_interface_qos(domxml)
    except Exception:
        return
    hooking.write_domxml(domxml)


if __name__ == '__main__':
    main()