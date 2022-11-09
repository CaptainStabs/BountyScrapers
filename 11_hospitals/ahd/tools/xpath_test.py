import requests
from lxml.html import fromstring


r = requests.get("https://www.ahd.com/free_profile/460006/")

p = fromstring(r.text)

print(p.xpath('//*[@itemprop="streetAddress"]/text()'))
print(p.xpath('//*[@itemprop="addressLocality"]/text()'))
print(p.xpath('//*[@itemprop="addressRegion"]/text()'))
print(p.xpath('//*[@itemprop="postalCode"]/text()'))
print(p.xpath('//*[@id="main"]/div[2]/table[1]/tr/td[1]/table/tr[8]/td[2]/text()'))
