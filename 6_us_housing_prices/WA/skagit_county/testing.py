import requests
from lxml.html import fromstring
from tqdm import tqdm



payload={}
headers = {
  'Cookie': 'ASP.NET_SessionId=4oh40r3srgv5iqvksyzdf00h'
}



for id in tqdm(range(1495, 5000)):
    id = "P" + str(id)
    url = f"https://skagitcounty.net/Search/Property/?id={id}"
    response = requests.request("GET", url, headers=headers, data=payload)

    parser = fromstring(response.text)

    try:
        parser.xpath('//*[@id="content_pdata"]/div[2]/text()')[0]

    except IndexError:
        print(id)
        break
