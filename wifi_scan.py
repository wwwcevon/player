#!/usr/local/bin/ve python
import requests
import time


KEVIN_IPHONE_MAC_ADDR = 'A8-5B-78-7A-92-50'

def main():
    is_online = False
    while True:
        res = mac_scan(KEVIN_IPHONE_MAC_ADDR)
        if not is_online and res:
            print(1)
            requests.post('http://127.0.0.1/next')
        elif is_online and res:
            print(2)
            pass
        elif not is_online and not res:
            print(3)
            pass
        elif is_online and not res:
            print(4)
            requests.post('http://127.0.0.1/stop')
        is_online = res

        time.sleep(1)


def mac_scan(mac_addr):
    url = 'http://192.168.10.1/userRpm/WlanStationRpm.htm?Page=1'
    headers = {
        'Host': '192.168.10.1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://192.168.10.1/userRpm/WlanStationRpm.htm?Page=1',
        'Authorization': 'Basic YWRtaW46YWRtaW4=',
        'Connection': 'keep-alive'
    }
    r = requests.get(url=url, headers=headers)
    res = mac_addr in r.text

    return res


if __name__ == '__main__':
    main()
