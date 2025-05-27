#!/usr/bin/python3

import sys
import hooking

try:
    domxml = hooking.read_domxml()
    redirdevs = domxml.getElementsByTagName('redirdev')

    for redirdev in redirdevs:
        sys.stderr.write("--usb redirdev = %s--" % redirdev.toxml())
        address = redirdev.getElementsByTagName('address')
        if address:
            address = address[0]
            redirdev.removeChild(address)

    hooking.write_domxml(domxml)
except:
    sys.stderr.write("--usb port remove failed!!--")