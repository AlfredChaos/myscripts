from xml.dom import minidom


encode_method = 'UTF-8'
doc = minidom.parseString("""
<interface type='bridge'>
    <mac address='56:6f:d8:26:00:0d'/>
    <source bridge='ovirtmgmt'/>
    <model type='virtio'/>
    <driver name='vhost' queues='4'/>
    <filterref filter='vdsm-no-mac-spoofing'/>
    <link state='up'/>
    <mtu size='1500'/>
    <alias name='ua-35411ddc-c2e4-49b9-b084-7ec999ff33b5'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
</interface>
""")
                          
interface = doc.getElementsByTagName('interface')[0]

# driver = doc.createElement('driver')
# driver.setAttribute('name', 'vhost')
# driver.setAttribute('queues', '4')
# interface.appendChild(driver)
# print(interface.toxml(encoding=encode_method))
driver = interface.getElementsByTagName('driver')[0]
driver.setAttribute('queues', '8')
driver.setAttribute('rx_queue_size', '1024')
driver.setAttribute('tx_queue_size', '1024')
print(interface.toxml(encoding=encode_method))