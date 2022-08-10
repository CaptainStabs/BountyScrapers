import re

pat = re.compile(r'(\d{3,4}\-\d{3,4})|(\d{3,4})')

string = "(Spanish (active France), 1881-1973)|Martin Fabiani, éditeur, Paris, 1942|etchings: Roger Lacourière, [Paris]; text: Fequet et Baudier, [Paris]|(French, 1707-1788)"

dates_pat = re.compile(r"(\d{3,4}\-\d{3,4})|(\d{3,4})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
born_pat = re.compile(r"(?: born )(\d{4})(?:\))")

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
            # print("years:", years)
            year_list.append([x for x in years])

        elif "/" not in bio:
            years = re.search(dates_pat, bio)
            year_list.append(years.group(0))

        elif "/" in bio:
            years = re.findall(pat1, bio)
            years = [tuple(y for y in tup if y != '') for tup in years]
            years = ["/".join(y) for y in years]

    b_list = []
    d_list = []
    for year in year_list:
        if "-" in year:
            b, d = year.split("-")
            b_list.append(b)
            d_list.append(d)
        else:
            b_list.append(year)
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

dates = ['(Spanish (active France), 1881-1973)', 'Martin Fabiani, éditeur, Paris, 1942', 'etchings: Roger Lacourière, [Paris]; text: Fequet et Baudier, [Paris]', '(French, 1707-1788)']
print(get_dates(dates))
