#!/usr/bin/python3

import hooking


def set_interface_queues(domxml):
    for iface in domxml.getElementsByTagName('interface'):
        driver = iface.getElementsByTagName('driver')[0]
        driver.setAttribute('queues', '8')
        driver.setAttribute('rx_queue_size', '1024')
        driver.setAttribute('tx_queue_size', '1024')


def main():
    domxml = hooking.read_domxml()
    set_interface_queues(domxml)
    hooking.write_domxml(domxml)


if __name__ == '__main__':
    main()