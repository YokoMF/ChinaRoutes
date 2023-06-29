import csv
from ipaddress import IPv4Network


class Node:
    def __init__(self, cidr, parent=None):
        self.cidr = cidr
        self.children = []
        self.dead = False
        self.parent = parent

    def __repr__(self):
        return "<Node %s>" % self.cidr


class AddressOfRegion:
    def __init__(self):
        self.root_v4 = list()
        self.root_v6 = list()
        with open("ipv4-address-space.csv", newline='') as fp:
            fp.readline()  # skip the title

            reader = csv.reader(fp, quoting=csv.QUOTE_MINIMAL)
            for cidr in reader:
                if cidr[5] == "ALLOCATED" or cidr[5] == "LEGACY":
                    block = cidr[0]
                    cidr = "%s.0.0.0%s" % (block[:3].lstrip("0"), block[-2:],)
                    self.root_v4.append(Node(IPv4Network(cidr)))

    @classmethod
    def mark_node(cls, nodes, anticidrs):
        """
        Mark cidr if it matches
        :param nodes: soruce nodes list.
        :param anticidrs: Exclude cidr list. If cidr in anticidrs matches in nodes list,
        then set node attribute to Ture.
        :return:
        """
        for anticidr in anticidrs:
            for node in nodes:
                if node.cidr == anticidr:
                    node.dead = True
                    break

                if node.cidr.supernet_of(anticidr):
                    if len(node.children) > 0:
                        cls.mark_node(node.children, anticidrs)
                    else:
                        node.children = [Node(ipadr, node) for ipadr in node.cidr.address_exclude(anticidr)]
                    break
