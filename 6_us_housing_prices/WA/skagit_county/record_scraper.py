import requests
import csv
from tqdm import tqdm
from lxml.html import fromstring
from dateutil import parser as dateparser



payload={}
headers = {
  'Cookie': 'ASP.NET_SessionId=4oh40r3srgv5iqvksyzdf00h'
}

columns = ["state", "physical_address", "county", "property_id", "sale_date", "property_type", "sale_price", "year_built", "source_url", "id"]
with open("records.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, fieldnames=columns)
    for id in tqdm(range(0, 5000)):
        id = "P" + str(id)
        url = f"https://skagitcounty.net/Search/Property/?id={id}"
        response = requests.request("GET", url, headers=headers, data=payload)

        parser = fromstring(response.text)


        land_info = {
            "state": "WA"
            "physical_address": " ".join(str(parser.xpath('//*[@id="content_pdata"]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td/text()')[0]).split()).upper().strip(),
            "county": " ".join(str(parser.xpath('//*[@id="jurisdiction"]/text()')[0]).split()).upper().strip(),
            "property_id": str(parser.xpath('//*[@id="content_pdata"]/table[2]/tbody/tr[2]/td[1]/b/text()')[0]).strip(),
            "sale_date": dateparser.parse(str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/text()')[0]).strip()),
            "property_type": " ".join(str(parser.xpath('//*[@id="content_pdata"]/table[7]/tbody/tr[6]/td[2]/text()')[0]).split()).upper().strip(),
            "sale_price": str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/text()')[0]).strip().replace("$", "").replace(",", "").split(".")[0],
            "year_built": str(parser.xpath('//*[@id="content_pdata"]/table[7]/tbody/tr[7]/td[2]/text()')).strip(),
            "source_url": url,
            "deed_type": str(parser.xpath('//*[@id="content_pdata"]/table[5]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/text()')[0]),
            "id": id
        }
