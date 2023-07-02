from modules.netcom import AddressOfRegion
from ipaddress import IPv4Network, IPv6Network
import math
from constconf import DEFAULTS, RESERVED
import argparse


def dump_nodes(nodes):
    """
    Traverse all leaf nodes(no children) which is not marked.
    :param nodes: nodes list
    :return:
    """
    for node in nodes:
        if node.dead:
            continue

        if len(node.children) > 0:
            dump_nodes(node.children)
        elif not node.dead:
            origins.append(node)


parser = argparse.ArgumentParser(description='Check ip if it is in the foreign IP list.')
parser.add_argument('ip', help='ip address')
args = parser.parse_args()

address_of_region = AddressOfRegion()
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
print("APNIC file process complete.")

with open(DEFAULTS['IPIPNET_FILE'], "r") as fipipnet:
    for line in fipipnet:
        line = line.strip('\n')
        item = IPv4Network(line)
        AddressOfRegion.mark_node(address_of_region.root_v4, (item,))
print("IPIPNET file process complete.")

AddressOfRegion.mark_node(address_of_region.root_v4, RESERVED)
print("IPV4 reserved address process complete.")

origins = []
ip = IPv4Network(args.ip)

dump_nodes(address_of_region.root_v4)

for node in origins:
    if node.cidr.supernet_of(ip):
        print(str(ip) + ' is subnet of ' + str(node.cidr))
