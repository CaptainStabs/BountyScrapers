import requests
from lxml import html

# r = requests.get("https://www.hsm.ox.ac.uk/collections-online#/browse-by-list/collection").text
with open("t.html", "r", encoding="utf-8") as f:
    r = f.read()
x = html.fromstring(r)
print(x.xpath('//*[@id="root"]/div[3]/div/a/div[2]/text()[2]'))
# '//*[@id="root"]/div[3]/div/a/div[2]/text()[2]'
