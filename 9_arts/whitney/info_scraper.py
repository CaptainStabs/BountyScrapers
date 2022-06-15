import requests
import pandas as pd
# from tqdm import tqdm
from lxml.html import fromstring
import swifter
import heartrate; heartrate.trace(browser=True, daemon=True)

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Cookie': '_whitney_session=Rzjk1H5HmEk4sGlFlcvZIe47x8rMlUBqlRsV956gSg6uAH4I7KAjX230090UFmBQM0JlvIb3zGDyYBDKHr2JzEa1pcE74yhLfvYa4YJSiPvpgH4NQEXExCRILBbu4yQRqk6xIXykIsbYt3E2oOInFPSNMhqvsN3mrCc4T9DAEXYxr8%2F%2F09BtNVYVQc8T8BKUXl2crTLo%2BLFXImYwy8po1Lf6ITyXB63eiPDs3ewfojuNE4czEXh%2F7E6U7KVNA2yogX%2BD3mylWc4RAnKTnWAGIjdkQh1zw65U--quTyHE19qEtwTiqs--ad2zzxmun1uRavhqi4uoog%3D%3D'
}
def search(art_id, maker, title):
    q = (str(maker.split("|")[0]) + " " + str(art_id)).replace(" ", "%20")
    url = f"https://whitney.org/search?q={q}"
    response = requests.request("GET", url, headers=headers)
    parser = fromstring(response.text)

    try:
        if parser.xpath('//*[@id="main"]/section/div[1]/ul[1]/li[1]/a/text()')[0] == "All (1)":
            return returner(parser)
        else:
            q = "%20".join([str(maker.split("|")[0]), str(title), str(art_id)]).replace(" ", "%20")
            url = f"https://whitney.org/search?q={q}"
            response = requests.request("GET", url, headers=headers)
            parser = fromstring(response.text)
            if parser.xpath('//*[@id="main"]/section/div[1]/ul[1]/li[1]/a/text()')[0] == "All (1)":
                return returner(parser)
            else:
                print(url)
                return ["", ""]
    except IndexError:
        with open("t.html", "w") as f:
            f.write(response.text)

def returner(parser):
    source_2 = "https://whitney.org" + str(parser.xpath('//*[@id="main"]/section/div[2]/div/ul/li/a/@href')[0])
    img_src = str(parser.xpath('//*[@id="main"]/section/div[2]/div/ul/li/a/div[1]/img/@src')[0])

    if img_src != "/assets/image_not_available-e1317b8a2d5139c81e2b0a42d92557c3be6fa2fc4d179bd5114cae9c1fb58222.svg":
        image_url = str(parser.xpath('//*[@id="main"]/section/div[2]/div/ul/li/a/div[1]/img/@src')[0])
    else:
        image_url = ""

    return [source_2, image_url]


df = pd.read_csv("output.csv")
df = df.head(20)
# tqdm.pandas()
df[['source_2', 'image_url']] = df.swifter.progress_bar(True, desc = "Scraping").apply(lambda x: search(x['accession_number'], x["maker_full_name"], x["title"]), axis=1, result_type='expand')
df.to_csv("output2.csv", index=False)
