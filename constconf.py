from ipaddress import IPv4Network, IPv6Network
import os


DEFAULTS = {
    'INTERFACE': "br-lan",
    'APNIC_URL': "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest",
    'APNIC_FILE': "delegated-apnic-latest",
    'IPIPNET_URL': "https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt",
    'IPIPNET_FILE': "china_ip_list",
    'IPV4CONF': "routes4.conf",
    'IPV6CONF': "routes6.conf",
    'HOST': "XXXX.XXXX.XXXX.XXXX",
    'PORT': 'XX',
    'USER': "XXX",
    'PASSWORD': "XXXXXX"
}

RESERVED = [
    IPv4Network('0.0.0.0/8'),
    IPv4Network('10.0.0.0/18'),
    IPv4Network('127.0.0.0/8'),
    IPv4Network('169.254.0.0/16'),
    IPv4Network('172.16.0.0/12'),
    IPv4Network('192.0.2.0/24'),
    IPv4Network('192.168.0.0/16'),
    IPv4Network('240.0.0.0/4'),
    IPv4Network('255.255.255.255/32'),
    IPv4Network('169.254.0.0/16'),
    IPv4Network('224.0.0.0/4'),
]
RESERVED_V6 = []
IPV6_UNICAST = IPv6Network('2000::/3')

for key, value in DEFAULTS.items():
    if os.getenv(key):
        DEFAULTS[key] = os.getenv(key)
