from xml.dom import minidom


encode_method = 'UTF-8'
doc = minidom.parseString("""
<interface type="bridge">
    <address bus="0x00" domain="0x0000" function="0x0" slot="0x03"\
                                        type="pci"/>
    <mac address="00:1a:4a:16:01:b0"/>
    <model type="virtio"/>
    <source bridge="ovirtmgmt"/>
    <filterref filter="vdsm-no-mac-spoofing"/>
    <link state="up"/>
    <boot order="1"/>
</interface>
""")
                          
interface = doc.getElementsByTagName('interface')[0]

driver = doc.createElement('driver')
driver.setAttribute('name', 'vhost')
driver.setAttribute('queues', '4')
interface.appendChild(driver)
print(interface.toxml(encoding=encode_method))