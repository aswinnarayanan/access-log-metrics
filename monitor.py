import sys
from urllib.parse import urlparse

import apache_log_parser
import geoip2.database
from netaddr import IPNetwork, IPAddress
from user_agents import parse

import json

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

_format = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
line_parser = apache_log_parser.make_parser(_format)


with open('blacklist.json') as f:
    CIDRS = json.load(f)


def in_block(ip, block):
        _ip = IPAddress(ip)
        return any([True
                    for cidr in block
                    if _ip in IPNetwork(cidr)])


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
    with open('output.csv', 'w+') as f:
        f.write('agent, ip_address, date, time, country, city, uri, agent_string')
        run = True
        while run:
            f.write('\n')
            try:
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                f.flush()
                break

            if not line:
                break

            req = line_parser(line)
            agent = parse(req['request_header_user_agent'])
            uri = urlparse(req['request_url']).path
            date = req['time_received_datetimeobj'].date()
            time = req['time_received_datetimeobj'].time()
            ip_address = req['remote_host']
            try:
                response = reader.city(req['remote_host'])
                country, city = response.country.name, response.city.name
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
                                      for network, cidr in CIDRS.items()
                                      if in_block(req['remote_host'], cidr)])

            entry = 'BOT' if is_bot else 'HUMAN', ip_address, date, time, country, city, uri, agent_str
            entry = tuple(map(str, entry))
            print(entry)
            f.write(','.join(entry))
