# import xml.etree.ElementTree as ET

# # 你的XML字符串
# xml_data = '''
# <devices>
#     <redirdev bus="usb" type="spicevmc">
#         <alias name="ua-f7743bd0-5e83-4f0b-b726-942fedcbeb7a" />
#         <address bus="0" port="1.4" type="usb" />
#     </redirdev>
#     <redirdev bus="usb" type="spicevmc">
#         <alias name="ua-caaf405d-cf99-489c-91ae-1e9331add83f" />
#         <address bus="0" port="1.3" type="usb" />
#     </redirdev>
# </devices>
# '''

# # 解析XML
# root = ET.fromstring(xml_data)

# # 遍历所有的redirdev标签
# for redirdev in root.findall('redirdev'):
#     # 找到address标签并删除
#     for address in redirdev.findall('address'):
#         redirdev.remove(address)

# # 将修改后的XML写入字符串
# modified_xml_data = ET.tostring(root, encoding='unicode', method='xml')

# print(modified_xml_data)

from xml.dom import minidom

# 你的XML字符串
xml_data = '''
<devices>
    <redirdev bus="usb" type="spicevmc">
        <alias name="ua-f7743bd0-5e83-4f0b-b726-942fedcbeb7a" />
        <address bus="0" port="1.4" type="usb" />
    </redirdev>
    <redirdev bus="usb" type="spicevmc">
        <alias name="ua-caaf405d-cf99-489c-91ae-1e9331add83f" />
        <address bus="0" port="1.3" type="usb" />
    </redirdev>
</devices>
'''

# 解析XML字符串
doc = minidom.parseString(xml_data)

# 找到所有的redirdev元素
for redirdev in doc.getElementsByTagName('redirdev'):
    # 找到address元素并删除
    address = redirdev.getElementsByTagName('address')[0]
    if address:
        redirdev.removeChild(address)

# 将修改后的XML写入字符串
modified_xml_data = doc.toprettyxml(indent="    ")

print(modified_xml_data)