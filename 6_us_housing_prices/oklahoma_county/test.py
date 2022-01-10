import requests
from lxml.html import fromstring
import json


headers = {
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Cookie': 'ASPSESSIONIDSQQAARDC=OLCJBOCALPJEDCDIOGHEIJEN'
}

url = f"https://docs.oklahomacounty.org/AssessorWP5/AN-R.asp?PropertyID=10"

s = requests.Session()
s.headers.update(headers)

response = s.request("GET", url, headers=headers)
parser = fromstring(response.text)

print(parser.xpath('/html/body/table[8]/thead/tr[1]/th/font/text()'))
# table = parser.xpath('//table[./thead/tr/th/font/text()="\r\n\t\t\tProperty Deed Transaction History\xa0\xa0 ("]/tbody/tr/td/p/font/text()')
table = parser.xpath('//table[./thead/tr/th/font/text()="\r\n\t\t\tProperty Deed Transaction History\xa0\xa0 ("]/tbody/tr')
land_info = {}
for row in table:
    print(str(row.xpath('./td[1]/p/font/text()')[0]).lstrip("\r\n\t\t\t"))
    land_info["sale_date"] = str(row.xpath('./td[1]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["type"] = str(row.xpath('./td[3]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["book"] = str(row.xpath('./td[4]/p/font/a/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["page"] = str(row.xpath('./td[5]/p/font/a/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["price"] = str(row.xpath('./td[6]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["seller_name"] = str(row.xpath('./td[5]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())
    land_info["buyer_name"] = str(row.xpath('./td[6]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())

# print(parser.xpath('//table/thead/tr/th/font/text()'))
land_info["year_built"] = str(parser.xpath('//table[./thead/tr/th/font/text()="Click \r\n\t\t\tbutton on building number to access \r\n\t\t\tdetailed information:"]/tbody/tr/td[5]/p/font/text()')[0].strip("\r\n\t\t\t").strip())
# print(parser.xpath('//table[./thead/tr/th/font/text()="Click \r\n\t\t\tbutton on building number to access \r\n\t\t\tdetailed information:"]/tbody/tr/td[5]/p/font/text()'))
print(json.dumps(land_info, indent=2))
