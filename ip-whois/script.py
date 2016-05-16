import urllib2
from bs4 import BeautifulSoup
from ipwhois import IPWhois
import socket
import pygeoip
from multiprocessing.pool import ThreadPool
import os
import time
from pprint import pprint


rawdata = pygeoip.GeoIP(os.path.abspath(os.path.join(os.path.dirname(__file__), 'GeoLiteCity.dat')))


def get_ip_data(ip_list):
    '''
    Provides data about IP addresses:
    - ISP Name
    - Country
    - BGP AS Number
    - Reverse DNS Lookup
    - Coordinates (x, y)
    - If ip is private according to RFC 1918

    :param ip_list: List of IP addresses
    :return: List of dictionaries with params 'ip', 'isp', 'country', 'asn', 'r_dns', 'x', 'y', 'private'
    '''
    ip_data = []
    for ip in ip_list:
        if not is_private(ip):
            try:
                country, asn = _get_country_asn(ip)
                x, y = _get_location(ip)
                item = {
                    'ip': ip,
                    'isp': _get_isp(ip),
                    'country': country,
                    'asn': asn,
                    'r_dns': _get_reverse_dns(ip),
                    'x': x,
                    'y': y,
                    'private': False
                }
                ip_data.append(item)
            except:
                pass
        else:
            item = {
                'ip': ip,
                'isp': None,
                'country': None,
                'asn': None,
                'r_dns': None,
                'x': None,
                'y': None,
                'private': True
            }
            ip_data.append(item)
    return ip_data


def _get_isp(ip):
    _base_url = 'https://www.whoismyisp.org/ip/'
    try:
        request = urllib2.Request(_base_url + ip, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib2.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')
        isp = soup.find('h1').text
        if isp == 'No ISP associated':
            isp = None
    except:
        isp = None
    finally:
        return isp


def _get_country_asn(ip):
    try:
        ip_data = IPWhois(ip).lookup_whois()
        country, asn = ip_data['asn_country_code'], 'AS' + ip_data['asn']
    except:
        country, asn = None, None
    finally:
        return country, asn


def _get_r_dns(*args):
    ip = ''.join(args)
    return socket.gethostbyaddr(ip)[0]


def _get_reverse_dns(ip):
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(_get_r_dns, (ip))
    try:
        # Regular request takes about 0.1 sec. If there are no redirect DNS it will take about 4 sec
        # To prevent a delay in case there are no redirect DNS, set a TIMEOUT
        TIMEOUT = 0.5
        r_dns = async_result.get(timeout=TIMEOUT)
    except:
        r_dns = None
    finally:
        return r_dns


def _get_location(ip):
    try:
        data = rawdata.record_by_name(ip)
        x, y = str(data['latitude']), str(data['longitude'])
    except:
        x, y = None, None
    finally:
        return x, y


def strip_ip(**kwargs):
    ip_list = kwargs['ip_list'].split('+')
    ips = []
    for ip in ip_list:
        try:
            _ip = ''
            for i, ip_part in enumerate(ip.split('.')):
                _ip += str(int(ip_part)) + '.'
                if i > 3:
                    break
            ips.append(_ip[:-1])
        except:
            pass
    return ips


def is_private(ip):
    '''
    According to RFC 1918, private IP address has range:
    10.0.0.0        -   10.255.255.255  (10/8 prefix)
    172.16.0.0      -   172.31.255.255  (172.16/12 prefix)
    192.168.0.0     -   192.168.255.255 (192.168/16 prefix)
    :param ip: IP address (str)
    :return: True - if IP is private, False - if IP is not private
    '''
    address = ip.split('.')
    if address[0] == '10':
        return True
    elif address[0] == '172':
        try:
            if 16 <= int(address[1]) <= 31:
                return True
        except:
            pass
    elif address[0] == '192' and address[1] == '168':
        return True


def get(list_of_ip):
    t0 = time.time()

    data = get_ip_data(list_of_ip)

    t1 = time.time() - t0
    print 'IPWHOIS request has took', t1, 'sec. for', len(list_of_ip), 'items.'
    return data


def main():
    ip = ['74.125.224.72', '69.59.196.211']
    data = get(ip)
    pprint(data)


if __name__ == '__main__':
    main()
