import requests
import lxml
from lxml import html

response = requests.get("https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1&InstName=ALDEN-HEBRON+HIGH+SCHOOL&City=HEBRON&County=MCHENRY&ID=170330000017")
with open("test.html", "w") as f:
    f.write(response.text)
tree = html.fromstring(response.content)
district = tree.xpath("/html/body/div/div[2]/div[3]/table/tbody/tr[19]/td/ol/li[1]/font/text()")
print("District: " + str(district))
print(district)
