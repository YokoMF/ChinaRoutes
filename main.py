import math
import paramiko
import argparse
from modules.netcom import AddressOfRegion
from modules.utilities import download_file, dump_bird
from constconf import DEFAULTS, RESERVED, RESERVED_V6
from ipaddress import IPv4Network, IPv6Network

parser = argparse.ArgumentParser(description='Generate non-China routes for BIRD.')
parser.add_argument('--sshremote', help='SSH to Remote', action="store_true")
args = parser.parse_args()

address_of_region = AddressOfRegion()
try:
    download_file(DEFAULTS['APNIC_URL'], DEFAULTS['APNIC_FILE'])
except:
    print("apnic file download failed! Skip download.")

try:
    download_file(DEFAULTS['IPIPNET_URL'], DEFAULTS['IPIPNET_FILE'])
except:
    print("ipipnet file download failed! Skip download.")

with open(DEFAULTS['APNIC_FILE'], "r") as fanpic:
    for line in fanpic:
        if "apnic|CN|ipv4|" in line:
            line = line.split("|")
            item = "%s/%d" % (line[3], 32 - math.log(int(line[4]), 2), )
            item = IPv4Network(item)
            AddressOfRegion.mark_node(address_of_region.root_v4, (item,))
        elif "apnic|CN|ipv6|" in line:
            line = line.split("|")
            item = "%s/%s" % (line[3], line[4])
            item = IPv6Network(item)
            AddressOfRegion.mark_node(address_of_region.root_v6, (item,))

with open(DEFAULTS['IPIPNET_FILE'], "r") as fipipnet:
    for line in fipipnet:
        line = line.strip('\n')
        item = IPv4Network(line)
        AddressOfRegion.mark_node(address_of_region.root_v4, (item,))

AddressOfRegion.mark_node(address_of_region.root_v4, RESERVED)
AddressOfRegion.mark_node(address_of_region.root_v6, RESERVED_V6)

with open(DEFAULTS['IPV4CONF'], "w") as fp4:
    dump_bird(address_of_region.root_v4, fp4)
with open(DEFAULTS['IPV6CONF'], "w") as fp6:
    dump_bird(address_of_region.root_v6, fp6)

if args.sshremote:
    transport = paramiko.Transport((DEFAULTS['HOST'], DEFAULTS['PORT']))  # 获取Transport实例
    transport.connect(username=DEFAULTS['USER'], password=DEFAULTS['PASSWORD'])  # 建立连接

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(DEFAULTS['IPV4CONF'], "/etc/routes4.conf")
    sftp.put(DEFAULTS['IPV6CONF'], "/etc/routes6.conf")

    transport.close()
