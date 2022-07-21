import requests
from lxml.html import fromstring
from tqdm import tqdm
from bs4 import BeautifulSoup
import re

dates_pat = re.compile(r"(\d{4}|\d{3} \d{4}|\d{3})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

def get_dates(dates):
    bio = "|".join(dates)
    if re.findall(pat2, bio):
        print("\nAAAA")
        years = bio.split(" - ")
        years = [y.replace("-", "/").strip("(").strip(")") for y in years]
        years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]

    elif re.findall(born_pat, bio):
        years = re.findall(born_pat, bio)

    elif "/" not in bio:
        years = re.findall(dates_pat, bio)
    elif "/" in bio:
        years = re.findall(pat1, bio)
        years = [tuple(y for y in tup if y != '') for tup in years]
        years = ["/".join(y) for y in years]


    birth_years = "|".join([years[i] for i in range(0, len(years), 2)])
    death_years = "|".join([years[i] for i in range(1, len(years), 2)])
    if len(birth_years):
        birth = birth_years
    else:
        birth = None
    if len(death_years):
        death = death_years
    else:
        death = None

    return birth, death


s = requests.Session()

r = s.get("http://emuseum.toledomuseum.org/objects/55041/")

soup = BeautifulSoup(r.text, "html.parser")

data = {}

parser = fromstring(r.text)

roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
names = [x.replace("\n", "") for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[1]/text()")]
dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

birth, death = None, None
if len(dates):
    birth, death = get_dates(dates)



print(birth, death)
print("Roles:", roles) # Remember to strip colons from roles
print("Names:", names)
# # for div in soup.find_all("div", attrs={'class': 'detail-item-details'}):
print("Title:", parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0])
print("Date:", parser.xpath("//*[@class='detailField displayDateField']/span[@class='detailFieldValue']/text()"))
print("Culture", parser.xpath("//*[@class='detailField cultureField']/span[@class='detailFieldValue']/text()")) # Culture
print("Materials:", parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()"))
print("Dimensions:", parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/div/text()"))
print("Category:", parser.xpath("//*[@class='detailField classificationField']/span[@class='detailFieldValue']/text()"))
print("Credit:", parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()"))
print("Num:", parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()"))
print("https://zimmerli.emuseum.com/" + str(parser.xpath('//*[@id="mediaZone"]/div/img/@src')))
print("Not on view:", parser.xpath("//*[@class='detailField currentLocationField']/text()"))
print("Cur Loc:", parser.xpath("//*[@class='detailField currentLocationField']/span[@class='detailFieldLabel']/text()"))
print("Description:",  parser.xpath("//*[@class='detailField labelTextField']/span[@class='detailFieldValue']/text()"))
print("Provenance:", parser.xpath('//*[@id="detailView"]/div[2]/div/div[11]/span[2]/text()'))
print(parser.xpath("//*[@class='emuseum-detail-category detailField collectionsField']/span[@class='detailFieldValue']/text()"))

desc_stuff = parser.xpath('//*[@class="detailField toggleField descriptionField"]/span[@class="toggleLabel detailFieldLabel"]/text()')
print(desc_stuff)

if "Provenance" in desc_stuff:
    prov_ind = desc_stuff.index("Provenance")
    print(prov_ind)
    prov = parser.xpath(f'//*[@class="detailField toggleField descriptionField"][{prov_ind+1}]/span[@class="toggleContent"]/text()')
    print(prov)
