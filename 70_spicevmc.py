#!/usr/bin/python3

import hooking


def remove_address(domxml):
    for redirdev in domxml.getElementsByTagName('redirdev'):
        # 找到address元素并删除
        address = redirdev.getElementsByTagName('address')[0]
        if address:
            redirdev.removeChild(address)


def main():
    domxml = hooking.read_domxml()
    remove_address(domxml)
    hooking.write_domxml(domxml)


if __name__ == '__main__':
    main()