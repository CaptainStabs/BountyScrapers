import requests
from lxml.html import fromstring
from tqdm import tqdm

s = requests.Session()
for i in tqdm(range(51246, 52000)):
    r = s.get("https://zimmerli.emuseum.com/objects/51275")

    parser = fromstring(r.text)

    artist = parser.xpath('//*[@id="detailView"]/div/div[2]/div/div/div[2]/span[1]/text()')

    if artist[0] != "Artist":
        print("NOT ARTIST")
        print(i)
        break

    classification = parser.xpath('//*[@id="detailView"]/div/div[2]/div/div/div[7]/span[1]/text()')[0]
    if classification != "Classifications":
        print("NOT CLASSIFICATION")
        print(i)
        break

        //*[@id="detailView"]/div/div[2]/div/div/div[2]/span[1]
        //*[@id="detailView"]/div/div[2]/div/div/div[2]/span[2]/span[1]
    # print(artist)
    # print(parser.xpath('//*[@id="detailView"]/div/div[2]/div/div/div[2]/span[2]/span[1]/text()')[0])
