import requests
from lxml.html import fromstring
import csv
import os
import usaddress
import json
import csv
from tqdm import tqdm


url = "https://docs.oklahomacounty.org/AssessorWP5/SalesSearch.asp"

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

columns = ["state", "sale_date", "map_num", "deed", "property_id", "res/com", "source_url", "city", "vac/imp", "property_type", "physical_address", "sale_price"]
with open("data.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)

    for year in tqdm(range(2015, 2021)):
        payload= f'AccountType=%25&AssessorMap=&BuildingDescription=&City=%25&Deed=%25&SaleDate={year}&fpdbr_4_PagingMove=%20%20%7C%3C%20%20&yes=%25'
        response = requests.request("POST", url, headers=headers, data=payload)

        # Parse in here
        parser = fromstring(response.text)
        page_limit = str(str(parser.xpath('/html/body/table[4]/tbody/tr[101]/td/form/nobr/text()')).split("/")[1]).strip("]'")
        for page in tqdm(range(int(page_limit))):
            # print("PAGE:", page)
            payload= f'AccountType=%25&AssessorMap=&BuildingDescription=&City=%25&Deed=%25&SaleDate={year}&fpdbr_4_PagingMove=%20%20%3E%20%20%20&yes=%25'
            response = requests.request("POST", url, headers=headers, data=payload)

            parser = fromstring(response.text)
            for row in range(1, 100):
                try:
                    # Parse in here
                    land_info = {
                        "state":"OK",
                        "sale_date": str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[1]/p/font/text()')[0]).lstrip("\r\n\t\t\t").upper(),
                        "map_num": str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[2]/p/font/text()')[0]).lstrip("\r\n\t\t\t"),
                        "deed": str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[3]/p/font/text()')[0]).lstrip("\r\n\t\t\t"),
                        "property_id": str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[4]/p/font/a/text()')[0]).lstrip("\r\n\t\t\t").upper(),
                        "res/com": str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[5]/p/font/text()')[0]).lstrip("\r\n\t\t\t"),
                        "source_url": "https://docs.oklahomacounty.org/AssessorWP5/"  + str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[4]/p/font/a/@href')[0]).lstrip("\r\n\t\t\t"),
                    }
                    try:
                        land_info["city"] =  " ".join(str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[6]/p/font/text()')[0]).lstrip("\r\n\t\t\t").replace("  ", " ").split()).upper()
                    except IndexError:
                        land_info["city"] = ""

                    # Probably doesn't need a block
                    try:
                        land_info["vac/imp"] = str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[7]/p/font/text()')[0]).lstrip("\r\n\t\t\t")
                    except IndexError:
                        land_info["vac/imp"] = ""

                    try:
                        land_info["property_type"] = str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[8]/p/font/text()')[0]).lstrip("\r\n\t\t\t").replace("  ", " ").strip().upper()
                    except IndexError:
                        land_info["property_type"] = ""

                    try:
                        land_info["physical_address"] = " ".join(str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[9]/p/font/text()')[0]).lstrip("\r\n\t\t\t").replace("  ", " ").strip().split()).upper()
                    except IndexError:
                        land_info["physical_address"] = ""

                    try:
                        land_info["sale_price"] = str(parser.xpath(f'/html/body/table[4]/tbody/tr[{row}]/td[10]/p/font/text()')[0]).lstrip("\r\n\t\t\t").strip().replace(",", "")
                    except IndexError:
                        land_info["sale_price"] = ""

                    writer.writerow(land_info)
                except IndexError as e:
                    print(e)
    # print(response.text)
