import requests
from lxml.html import fromstring
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import polars as pl

pl.Config.set_tbl_rows(150)
pl.Config.set_fmt_str_lengths(4000)
pl.Config.set_tbl_cols(500)
dates_pat = re.compile(r"(\d{3,4}\-\d{3,4})|(\d{3,4})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})\)")

# print(re.findall(pat, string))

def get_dates(dates: list) -> tuple:
    year_list = []
    for bio in dates:
        if not any(x.isdigit() for x in bio):
            year_list.append("")
            continue

        print("Bio:",bio)
        if re.findall(pat2, bio):
            print("\nAAAA")
            years = bio.split(" - ")
            years = [y.replace("-", "/").strip("(").strip(")") for y in years]
            years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]
            year_list.append([x for x in years])

        elif re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)
            print("QQQQ",years)
            # print("years:", years)
            print("LEN", len(years))
            year_list.extend(years)
            print("AAA", year_list)

        elif "/" not in bio:
            years = re.search(dates_pat, bio)
            if years:
                print("QQQQ",years.group(0))
                year_list.append(years.group(0))

        elif "/" in bio:
            years = re.findall(pat1, bio)
            years = [tuple(y for y in tup if y != '') for tup in years]
            years = ["/".join(y) for y in years]

    print(year_list)
    b_list = []
    d_list = []
    for year in year_list:
        if "-" in year:
            b, d = year.split("-")
            b_list.append(b)
            d_list.append(d)
        else:
            print("YEATTTT", year)
            b_list.append(year)
            d_list.append("")

    print(year_list)
    birth_years = "|".join(b_list)
    death_years = "|".join(d_list)
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

r = s.get("http://emuseum.toledomuseum.org/objects/55248")

data = {}

parser = fromstring(r.text)

roles = parser.xpath("//div[@class='detailField peopleField']/*/text()")
names = [x.replace("\n", "") for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[1]/text()")]
dates = [x.replace("\n", "").strip() for x in parser.xpath("//div[@class='detailField peopleField']/span[2]/span[last()]/text()")]

birth, death = None, None
if len(dates):
    birth, death = get_dates(dates)

print(parser.xpath("//*[@class='detailField currentLocationField']/text()"))
data = [{
        "title": str(parser.xpath('//*[@class="detailField titleField"]/h1/text()')[0]),
        "Birth": birth,
        "death": death,
        "names": "|".join(names) if names else None,
        "roles": "|".join(roles),
        "date": str(parser.xpath("//*[@class='detailField displayDateField']/span[@class='detailFieldValue']/text()")),
        "dimensions": str(parser.xpath("//*[@class='detailField dimensionsField']/span[@class='detailFieldValue']/div/text()")),
        "materials": str(parser.xpath("//*[@class='detailField mediumField']/span[@class='detailFieldValue']/text()")),
        "category": str(parser.xpath("//*[@class='detailField classificationField']/span[@class='detailFieldValue']/text()")),
        "credit": str(parser.xpath("//*[@class='detailField creditlineField']/span[@class='detailFieldValue']/text()")),
        "num": str(parser.xpath("//*[@class='detailField invnoField']/span[@class='detailFieldValue']/text()")),
        "description": str(parser.xpath("//*[@class='detailField labelTextField']/span[@class='detailFieldValue']/text()")),
        "not on view": str(parser.xpath("//*[@class='detailField currentLocationField']/text()")),
        "cur loc": str(": ".join([parser.xpath("//*[@class='detailField currentLocationField']/span[@class='detailFieldLabel']/text()")[0], parser.xpath("//*[@class='detailField currentLocationField']/span[@class='detailFieldValue']/text()")[0].replace("\n", "").strip()])),
        "culture": str(parser.xpath("//*[@class='detailField cultureField']/span[@class='detailFieldValue']/text()")),
        "provenance": str(parser.xpath('//*[@id="detailView"]/div[2]/div/div[11]/span[2]/text()')),
        "from_location": str(parser.xpath('//*[@class="detailField periodField"]/span[@class="detailFieldValue"]/text()'))
}]

df = pl.DataFrame(data)
df = df.transpose(include_header=True)

df["column"] = df["column"].str.rjust(10, " ")
print(df)

print("https://zimmerli.emuseum.com/" + str(parser.xpath('//*[@id="mediaZone"]/div/img/@src')))

desc_stuff = parser.xpath('//*[@class="detailField toggleField descriptionField"]/span[@class="toggleLabel detailFieldLabel"]/text()')
print(desc_stuff)

if "Description" in desc_stuff:
    desc_ind = desc_stuff.index("Description")
    desc = parser.xpath(f'//*[@class="detailField toggleField descriptionField"][{desc_ind+1}]/span[@class="toggleContent"]/text()')
    print(desc)
