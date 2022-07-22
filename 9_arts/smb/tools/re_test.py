import re

dates_pat = re.compile(r"((?<=\.)(\d{3,4})( - ).*?(?<=\.)(\d{3,4}))")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

# print(re.findall(pat, string))

def get_dates(dates: list, url) -> tuple:
    year_list = []
    for bio in dates:
        if not any(x.isdigit() for x in bio):
            year_list.append("")
            continue

        if re.findall(born_pat, bio):
            years = re.findall(born_pat, bio)
            # print("years:", years)
            year_list.append([x for x in years])

        elif "/" not in bio and re.findall(dates_pat, bio):
            years = re.findall(dates_pat, bio)[0]
            year_list.append("".join(years[1:]))

        elif "/" in bio:
            year_list.append("")
            continue

        else:
            print("UNKNOWN FORMAT:", bio, url)
            year_list.append("")
            continue

    b_list = []
    d_list = []
    for year in year_list:
        if "-" in year:
            b, d = year.split("-")
            b_list.append(b.strip())
            d_list.append(d.strip())
        else:
            b_list.append(year.strip())
            d_list.append("")

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

dates = ['S.M.S. Cormoran (25.7.1893 - 6.8.1914), Expedition']
print(get_dates(dates, "a"))
