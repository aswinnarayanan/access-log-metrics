import sys
from urlparse import urlparse

import apache_log_parser
from colorama import Back, Style
import geoip2.database
from netaddr import IPNetwork, IPAddress
from user_agents import parse


reader = geoip2.database.Reader('GeoLite2-City.mmdb')

_format = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
line_parser = apache_log_parser.make_parser(_format)

CIDRS = {
    'Amazon': ['107.20.0.0/14', '122.248.192.0/19', '122.248.224.0/19',
               '172.96.96.0/20', '174.129.0.0/16', '175.41.128.0/19',
               '175.41.160.0/19', '175.41.192.0/19', '175.41.224.0/19',
               '176.32.120.0/22', '176.32.72.0/21', '176.34.0.0/16',
               '176.34.144.0/21', '176.34.224.0/21', '184.169.128.0/17',
               '184.72.0.0/15', '185.48.120.0/26', '207.171.160.0/19',
               '213.71.132.192/28', '216.182.224.0/20', '23.20.0.0/14',
               '46.137.0.0/17', '46.137.128.0/18', '46.51.128.0/18',
               '46.51.192.0/20', '50.112.0.0/16', '50.16.0.0/14', '52.0.0.0/11',
               '52.192.0.0/11', '52.192.0.0/15', '52.196.0.0/14',
               '52.208.0.0/13', '52.220.0.0/15', '52.28.0.0/16', '52.32.0.0/11',
               '52.48.0.0/14', '52.64.0.0/12', '52.67.0.0/16', '52.68.0.0/15',
               '52.79.0.0/16', '52.80.0.0/14', '52.84.0.0/14', '52.88.0.0/13',
               '54.144.0.0/12', '54.160.0.0/12', '54.176.0.0/12',
               '54.184.0.0/14', '54.188.0.0/14', '54.192.0.0/16',
               '54.193.0.0/16', '54.194.0.0/15', '54.196.0.0/15',
               '54.198.0.0/16', '54.199.0.0/16', '54.200.0.0/14',
               '54.204.0.0/15', '54.206.0.0/16', '54.207.0.0/16',
               '54.208.0.0/15', '54.210.0.0/15', '54.212.0.0/15',
               '54.214.0.0/16', '54.215.0.0/16', '54.216.0.0/15',
               '54.218.0.0/16', '54.219.0.0/16', '54.220.0.0/16',
               '54.221.0.0/16', '54.224.0.0/12', '54.228.0.0/15',
               '54.230.0.0/15', '54.232.0.0/16', '54.234.0.0/15',
               '54.236.0.0/15', '54.238.0.0/16', '54.239.0.0/17',
               '54.240.0.0/12', '54.242.0.0/15', '54.244.0.0/16',
               '54.245.0.0/16', '54.247.0.0/16', '54.248.0.0/15',
               '54.250.0.0/16', '54.251.0.0/16', '54.252.0.0/16',
               '54.253.0.0/16', '54.254.0.0/16', '54.255.0.0/16',
               '54.64.0.0/13', '54.72.0.0/13', '54.80.0.0/12', '54.72.0.0/15',
               '54.79.0.0/16', '54.88.0.0/16', '54.93.0.0/16', '54.94.0.0/16',
               '63.173.96.0/24', '72.21.192.0/19', '75.101.128.0/17',
               '79.125.64.0/18', '96.127.0.0/17'],
    'Baidu': ['180.76.0.0/16', '119.63.192.0/21', '106.12.0.0/15',
              '182.61.0.0/16'],
    'DO': ['104.131.0.0/16', '104.236.0.0/16', '107.170.0.0/16',
           '128.199.0.0/16', '138.197.0.0/16', '138.68.0.0/16',
           '139.59.0.0/16', '146.185.128.0/21', '159.203.0.0/16',
           '162.243.0.0/16', '178.62.0.0/17', '178.62.128.0/17',
           '188.166.0.0/16', '188.166.0.0/17', '188.226.128.0/18',
           '188.226.192.0/18', '45.55.0.0/16', '46.101.0.0/17',
           '46.101.128.0/17', '82.196.8.0/21', '95.85.0.0/21', '95.85.32.0/21'],
    'Dream': ['173.236.128.0/17', '205.196.208.0/20', '208.113.128.0/17',
              '208.97.128.0/18', '67.205.0.0/18'],
    'Google': ['104.154.0.0/15', '104.196.0.0/14', '107.167.160.0/19',
               '107.178.192.0/18', '108.170.192.0/20', '108.170.208.0/21',
               '108.170.216.0/22', '108.170.220.0/23', '108.170.222.0/24',
               '108.59.80.0/20', '130.211.128.0/17', '130.211.16.0/20',
               '130.211.32.0/19', '130.211.4.0/22', '130.211.64.0/18',
               '130.211.8.0/21', '146.148.16.0/20', '146.148.2.0/23',
               '146.148.32.0/19', '146.148.4.0/22', '146.148.64.0/18',
               '146.148.8.0/21', '162.216.148.0/22', '162.222.176.0/21',
               '173.255.112.0/20', '192.158.28.0/22', '199.192.112.0/22',
               '199.223.232.0/22', '199.223.236.0/23', '208.68.108.0/23',
               '23.236.48.0/20', '23.251.128.0/19', '35.184.0.0/14',
               '35.188.0.0/15', '35.190.0.0/17', '35.190.128.0/18',
               '35.190.192.0/19', '35.190.224.0/20', '8.34.208.0/20',
               '8.35.192.0/21', '8.35.200.0/23',],
    'Hetzner': ['129.232.128.0/17', '129.232.156.128/28', '136.243.0.0/16',
                '138.201.0.0/16', '144.76.0.0/16', '148.251.0.0/16',
                '176.9.12.192/28', '176.9.168.0/29', '176.9.24.0/27',
                '176.9.72.128/27', '178.63.0.0/16', '178.63.120.64/27',
                '178.63.156.0/28', '178.63.216.0/29', '178.63.216.128/29',
                '178.63.48.0/26', '188.40.0.0/16', '188.40.108.64/26',
                '188.40.132.128/26', '188.40.144.0/24', '188.40.48.0/26',
                '188.40.48.128/26', '188.40.72.0/26', '196.40.108.64/29',
                '213.133.96.0/20', '213.239.192.0/18', '41.203.0.128/27',
                '41.72.144.192/29', '46.4.0.128/28', '46.4.192.192/29',
                '46.4.84.128/27', '46.4.84.64/27', '5.9.144.0/27',
                '5.9.192.128/27', '5.9.240.192/27', '5.9.252.64/28',
                '78.46.0.0/15', '78.46.24.192/29', '78.46.64.0/19',
                '85.10.192.0/20', '85.10.228.128/29', '88.198.0.0/16',
                '88.198.0.0/20'],
    'Linode': ['104.200.16.0/20', '109.237.24.0/22', '139.162.0.0/16',
               '172.104.0.0/15', '173.255.192.0/18', '178.79.128.0/21',
               '198.58.96.0/19', '23.92.16.0/20', '45.33.0.0/17',
               '45.56.64.0/18', '45.79.0.0/16', '50.116.0.0/18',
               '80.85.84.0/23', '96.126.96.0/19'],
}


def in_block(ip, block):
        return any([True
                    for cidr in block
                    if IPAddress(ip) in IPNetwork(cidr)])


def bot_test(req, agent):
        ua_tokens = ['daum/', # Daum Communications Corp.
                     'gigablastopensource',
                     'go-http-client',
                     'http://',
                     'httpclient',
                     'https://',
                     'libwww-perl',
                     'phantomjs',
                     'proxy',
                     'python',
                     'sitesucker',
                     'wada.vn',
                     'webindex',
                     'wget']

        is_bot = agent.is_bot or \
                 any([True
                      for cidr in CIDRS.values()
                      if in_block(req['remote_host'], cidr)]) or \
                 any([True
                      for token in ua_tokens
                      if token in agent.ua_string.lower()])

        return is_bot


if __name__ == '__main__':
    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break

        req = line_parser(line)
        agent = parse(req['request_header_user_agent'])
        uri = urlparse(req['request_url'])

        try:
            response = reader.city(req['remote_host'])
            country, city = response.country.iso_code, response.city.name
        except:
            country, city = None, None

        is_bot = bot_test(req, agent)

        agent_str = ''.join([item
                             for item in agent.browser[0:3] +
                                         agent.device[0:3] +
                                         agent.os[0:3]
                             if item is not None and
                                type(item) is not tuple and
                                len(item.strip()) and
                                item != 'Other'])

        ip_owner_str = ', '.join([network + ' IP'
                                  for network, cidr in CIDRS.iteritems()
                                  if in_block(req['remote_host'], cidr)])

        print Back.RED + 'b' if is_bot else 'h', \
              country, \
              city, \
              uri.path, \
              agent_str, \
              ip_owner_str, \
              Style.RESET_ALL