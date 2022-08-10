import requests
from lxml.html import fromstring
from tqdm import tqdm
from bs4 import BeautifulSoup
import re

s = requests.Session()

r = s.get("https://collections.peabody.harvard.edu/objects/details/270675")

soup = BeautifulSoup(r.text, "html.parser")

data = {}

parser = fromstring(r.text)
#
# roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
# names = [x.replace("\n", "") for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[@property='name']/text()")]
# dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]
#
# birth, death = None, None
# if len(dates):
#     birth, death = get_dates(dates)

# print(birth, death)
# print("Roles:", roles) # Remember to strip colons from roles
# print("Names:", names)
# # for div in soup.find_all("div", attrs={'class': 'detail-item-details'}):

print("Title:", parser.xpath('//*[@class="detailField titleField"]/span[@class="detailFieldValue"]/text()')[0].replace("\n", "").strip())
print("Date", parser.xpath("//*[@class='detailField displayDateField']/span[@property='dateCreated']/text()")[0].replace("\n", "").strip())
# print("Materials:", parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/a/text()"))
# print("Culture:", " ".join(parser.xpath("//*[@class='emuseum-detail-category detailField thesconceptsField']/text()")).replace("\n\t", "").strip(), "END.") # Culture
print("Dimensions:", parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/text()"))
# print("Classification", parser.xpath("//*[@class='detailField classificationField']/span[@class='detailFieldValue']/text()"))
# print("Credit:", parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()"))
print("Num:", parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()"))
# print("https://zimmerli.emuseum.com/" + str(parser.xpath('//*[@id="mediaZone"]/div/img/@src')))
# print("Category:", parser.xpath("//*[@class='detailField multiItemField classificationsField']/div/text()"))
# print("Cur Loc:", parser.xpath("//*[@class='detailField onviewField']/div/text()"))
print("Description:",  parser.xpath('//*[@class="detailField titleField paragraph2"]/span[2]/text()'))
# print("Provenance:", parser.xpath('//*[@id="detailView"]/div[2]/div/div[11]/span[2]/text()'))
# print(parser.xpath("//*[@class='emuseum-detail-category detailField collectionsField']/span[@class='detailFieldValue']/text()"))
print("Department:", parser.xpath("//*[@class='detailField departmentField']/span[@class='detailFieldValue']/a/text()"))
print("Maker name:", parser.xpath("//*[@class='detailField peopleField']/span[@class='detailFieldValue']/span/text()"))
print("Location:", parser.xpath("//*[@class='thes-path-flat']/div/div/span/text()"))
#
# desc_stuff = [x.replace("\n", "").strip() for x in parser.xpath('//*[@class="emuseum-detail-category detailField thesconceptsField"]/span[@class="detailFieldLabel"]/text()')]
# print(desc_stuff)
# culture = None
# if "Culture" in desc_stuff:
#     cult_ind = desc_stuff.index("Culture")
#     cult = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cult_ind+1}]/ul/li/span/text()')
# if "Classification" in desc_stuff:
#     cate_ind = desc_stuff.index("Classification")
#     cate = parser.xpath(f'//*[@class="emuseum-detail-category detailField thesconceptsField"][{cate_ind+1}]/ul/li/span/text()')
#
# print(cate)
#
# prov_stuff = parser.xpath("//*[@class='detailField peopleField paragraph2']/span/span[@property='name']/text()")
# prov_stuff = [x.replace("\n", "").strip() for x in prov_stuff]
# print(prov_stuff)
# # prov_stuff = [' '.join(x) for x in zip(prov_stuff[0::2], prov_stuff[1::2])]
#
# prov_role = parser.xpath("//*[@class='detailField peopleField paragraph2']/span[@class='detailFieldLabel']/text()")
# print(prov_role)
#
# result = [i + ': ' + j for i in prov_role for j in prov_stuff]
#
# print(result)
