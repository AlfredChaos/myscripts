#!/usr/bin/python3

import hooking


def set_disk_qos(domxml):
    for disk in domxml.getElementsByTagName('disk'):
        if disk.getAttribute('device') != 'disk':
            continue
        iotune_node = domxml.createElement('iotune')

        read_node = domxml.createElement('read_iops_sec')
        value = domxml.createTextNode('2048')
        read_node.appendChild(value)
        iotune_node.appendChild(read_node)

        write_node = domxml.createElement('write_iops_sec')
        value = domxml.createTextNode('2048')
        write_node.appendChild(value)
        iotune_node.appendChild(write_node)

        disk.appendChild(iotune_node)


def main():
    domxml = hooking.read_domxml()
    try:
        set_disk_qos(domxml)
    except Exception:
        return
    hooking.write_domxml(domxml)


if __name__ == '__main__':
    main()