import re
from dateutil import parser as dateparser

dates_pat = re.compile(r"(\d{3,4}(?:\-|\–)\d{3,4})")
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
            years = bio.replace("–", "-").split("-")
            years = [y.replace("-", "/").strip("(").strip(")").strip(   ) for y in years]
            years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]
            year_list.append([x for x in years])

        elif re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)
            print("QQQQ",years)
            # print("years:", years)
            print("LEN", len(years))
            year_list.extend(years)
            print("AAA", year_list)

        elif "/" not in bio and re.findall(dates_pat, bio):
            print("BBB")
            years = re.findall(dates_pat, bio)[0]
            years = years.replace("–", "-")#.split("-")
            year_list.append(years)

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

dates = [["James Monroe Hewlett (American artist and architect, 1868–1941)", "Sackett & Wilhelms Corp. (New York printing firm, 1889–1950)"]]
for date in dates:
    print(date)
    print(get_dates(date))
    print("\n")
