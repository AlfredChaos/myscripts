import random
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp

# 报文的时间戳、源MAC和目的MAC（广播）
src_mac = "4e:04:f8:07:e9:d0"
dst_mac = "ff:ff:ff:ff:ff:ff"
xid = random.randint(1, 0xFFFF)  # 事务ID

# 创建以太网帧
ether = Ether(dst=dst_mac, src=src_mac)

# 创建IP头部
ip = IP(dst="255.255.255.255", src="0.0.0.0", flags="DF")

# 创建UDP头部
udp = UDP(sport=68, dport=67)

# 创建BOOTP部分
bootp = BOOTP(op=1, chaddr=src_mac, xid=xid, flags=0x8000)  # 广播标志为0，表示单播

client_id = bytearray.fromhex("01") + bytes.fromhex(src_mac.replace(":", ""))

# 创建DHCP选项
options = [
    ("message-type", "request"),
    ("requested_addr", "10.123.1.226"),
    ("hostname", "5253FC7506FA"),
    ("client_id", client_id),
    ("param_req_list", [1, 3, 6, 15])
]
dhcp = DHCP(options=options)

# 封装报文
packet = ether / ip / udp / bootp / dhcp

# 打印报文信息
#packet.show()

# 发送报文
sendp(packet, iface="p2", count=1)  # 注释掉的代码用于实际发送