import requests
from lxml.html import fromstring
from tqdm import tqdm
from bs4 import BeautifulSoup

s = requests.Session()

r = s.get("https://zimmerli.emuseum.com/objects/23849")

soup = BeautifulSoup(r.text, "html.parser")

data = {}

parser = fromstring(r.text)

roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
names = [x.replace("\n", "") for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[@property='name']/text()")]
dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

print(roles)
print(names)
print(dates)
# for div in soup.find_all("div", attrs={'class': 'detail-item-details'}):
