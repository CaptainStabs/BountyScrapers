import requests
import csv
import os
import sys
from lxml.html import fromstring
from tqdm import tqdm
import pandas as pd


payload={}
headers = {
  'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document'
}
columns = ["name", "business_type", "state_registered", "state_physical", "street_physical", "city_physical","zip5_physical", "filing_number", "corp_id"]

filename = "arkansas.csv"

# df = pd.read_csv(filename)
# df_columns = list(df.columns)
# data_columns = ",".join(map(str, df_columns))
#
# # Get the last row from df
# last_row = df.tail(1)
# # Access the corp_id
# last_id = last_row["corp_id"].values[0]

with open(filename, "w", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    # for detail_id in tqdm(range(1, 607920)):
    detail_id = 340105
    # Convert the int to a left-padded str compatible with website
    detail_padded = str(detail_id).zfill(6)
    # Put detail_id into url
    # url = f"https://www.sos.arkansas.gov/corps/search_corps.php?DETAIL={detail_padded}"
    # response = requests.request("GET", url, headers=headers, data=payload)

    # Parse the html with lxml.html's fromstring
    # print(response.text
    with open("test5.html", "r") as html_file:
        read_html = html_file.readlines()
    parser = fromstring(html_file)

    print(parser.xpath('/html/body/div[2]/div/div[2]/div/table[2]/tbody/tr[2]/td[2]/font'))
    print(str(parser.xpath('//*[@id="results"]/table[2]/tr[2]/td[1]/font/text()')))
    print(str(parser.xpath('//*[@id="mainContent"]/table[2]/tr[16]/text()')))
    print(str(parser.xpath('//*[@id="mainContent"]/table[2]/tr[7]/td[2]/font/text()')))
    # break
    # Initilalize dict
    # business_info = {}
    #
    # if str(parser.xpath('//*[@id="mainContent"]/table[2]/tbody/tr[7]/td[2]/font/text()')).upper().strip
