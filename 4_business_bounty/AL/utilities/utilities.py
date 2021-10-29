import requests
from lxml.html import fromstring
from more_itertools import random_permutation
from itertools import cycle


# Some code lifted from a tutorial on creating rotating IP set for scraping
#   https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()

    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            print(proxy)
            proxies.add(proxy)
    with open("proxies.txt", "a") as f:
        print("Num of proxies: " + str(len(proxies)))
        f.write(str(list(proxies)))

    return random_permutation(list(proxies))


def get_proxy_cycle():
    return cycle(get_proxies())

def open_proxy_cycle():
    with open("proxies.txt", "r") as f:
        lines = f.readline()
        lines = lines.replace("\n", "").replace(" ", "").replace("'", "").strip("[]")
        proxy_list = lines.split(",")
        # print(proxy_list)
    return random_permutation(list(proxy_list))

def get_open_proxy_cycle():
    return cycle(open_proxy_cycle())

# for i in range(20):
#     print(next(get_open_proxy_cycle()))

# get_proxies()
