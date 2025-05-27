from xml.dom import minidom


encode_method = 'UTF-8'
doc = minidom.parseString("""
<disk type='network' device='cdrom' snapshot='no'>
    <driver name='qemu' type='raw' cache='none'/>
    <source protocol='rbd' name='raystack/delete'>
        <host name='10.123.10.224' port='6789'/>
        <host name='10.123.10.225' port='6789'/>
        <host name='10.123.10.226' port='6789'/>
    </source>
    <target dev='sda' bus='scsi'/>
    <serial>540fdc2c-5d65-443a-9f84-c3424ee0b309</serial>
    <alias name='ua-a96b160d-fb99-43c5-966a-0fc706f196b1'/>
</disk>
""")

dom=minidom.Document()                     
disks = doc.getElementsByTagName('disk')
for d in disks:
    print(d.getAttribute('device'))
    if d.getAttribute('device') != 'disk':
        continue
    iotune_node = dom.createElement('iotune')

    read_node = dom.createElement('read_iops_sec')
    value = dom.createTextNode('2048')
    read_node.appendChild(value)
    iotune_node.appendChild(read_node)

    write_node = dom.createElement('write_iops_sec')
    value = dom.createTextNode('2048')
    write_node.appendChild(value)
    iotune_node.appendChild(write_node)

    d.appendChild(iotune_node)
    print(d.toxml(encoding=encode_method))