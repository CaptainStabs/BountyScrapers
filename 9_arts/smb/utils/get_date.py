import re

dates_pat = re.compile(r"((?:(?<=\.)|(?<=\()|(?<=\(um )|(?<=\(ca\. ))\d{3,4}(?: - |-)(?:.*?(?<=\.)(?:\d{3,4})|(?:\d{3,4})))")
dates_pat2 = re.compile(r"(\d{3,4}(?: - |-)\d{3,4})")
single_date = re.compile(r"((?<=\()(?:\d{3,4})(?=\))|(?<=\()(?:\d{1,2}\.\d{1,2}\.\d{3,4})(?=\)))")
born_pat = re.compile(r"(?<=\()(\d{3,4}(?: - | -|-))(?:(?=u)|(?=\)))")
ca_nach = re.compile(r"((?:\d{3,4}(?: - |-)(?:nach) \d{3,4})|(?<=\(\(nach\) )\d{3,4})")
death_pat = re.compile(r"((?<=\( - )|(?<=\(-))(\d{3,4})(?=\))")

# print(re.findall(pat, string))

def get_dates(dates: list, url) -> tuple:
    year_list = []
    for bio in dates:
        if not any(x.isdigit() for x in bio):
            year_list.append("b")
            continue

        bio = bio.replace("† ", "")

        if re.findall(dates_pat2, bio):
            years = re.findall(dates_pat2, bio)[0]
            year_list.append(years)

        elif re.findall(single_date, bio) and re.findall(single_date, bio)[0] != '':
            years = re.search(single_date, bio).group(0)
            year_list.append(years)

        elif re.findall(ca_nach, bio):
            years = re.findall(ca_nach, bio)[0].replace("nach", "")
            year_list.append(years)

        elif "/" not in bio and re.findall(dates_pat, bio):
            years = re.findall(dates_pat, bio)[0]
            year_list.append(years)

        elif re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)[0].split("-")[0].strip()
            year_list.append(years)

        elif re.findall(death_pat, bio):
            years = re.findall(death_pat, bio)[0]
            year_list.append(years)

        elif "/" in bio:
            year_list.append("b")
            continue

        else:
            with open("unknown_formats.txt", "a") as f:
                f.write(str(bio), str(url))
            # print("\nUNKNOWN FORMAT:", bio, url)
            year_list.append("b")
            continue

    b_list = []
    d_list = []
    # print("LIST", year_list)
    for year in year_list:
        if not year:
            continue
        elif year == "b":
            b_list.append("")
            d_list.append("")
            continue

        if "-" in year:
            # print("YEAR", year)
            b, d = year.split("-")
            try:
                b, d = dateparser.parse(b.strip()), dateparser.parse(d.strip())
            except:
                b, d = dateparser.parse(b.strip().split(".")[-1]), dateparser.parse(d.strip().split(".")[-1])
            b_list.append(str(b.year))
            d_list.append(str(d.year))
        else:
            # print("YEAR2:", year)
            year = dateparser.parse(year.strip())
            b_list.append(str(year.year))
            d_list.append("")


    birth_years = "|".join(b_list)
    death_years = "|".join(d_list)
    # print(birth_years, death_years)
    if len(b_list):
        birth = birth_years
    else:
        birth = None
    if len(d_list):
        death = death_years
    else:
        death = None
    return birth, death
