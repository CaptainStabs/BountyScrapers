import requests
from lxml.html import fromstring
from tqdm import tqdm



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

def find_min(configs):
    start_id = configs["start_id"]
    end_id = configs["end_id"]
    scraper_number = configs["scraper_number"]
    for id in tqdm(range(0, 1500000000)):
        url = f"https://www.sos.ok.gov/corp/corpInformation.aspx?id={id}"
        response = requests.request("GET", url, headers=headers, data=payload)
        parser = fromstring(response.text)
        if "RECORD NOT FOUND" in str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()')[0]).upper():
            continue
        else:
            print("   [!!!] Scraper " + str(scraper_number) + " has finished!")
            print("   [*] ID: " + str(id))
            print(str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()')[0]).upper())
            print("   [*] url: " + str(url))
            break
        # print(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()'))

        # print(response.text)
