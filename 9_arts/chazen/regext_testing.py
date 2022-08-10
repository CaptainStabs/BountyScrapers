import re

tests = [
"active ca. 470-ca. 460 B.C.E.",
"(American, b. 1972)",
"(American, 1851 - 1914)",
"(English)",
]
pat = re.compile(r"(\d{4}|\d{3} \d{4}|\d{3})")
pat1 = re.compile(r"(?:(?:(\d{4}|\d{3})\/)|(:?|\d{4}|\d{3}))(?:(\d{4}|\d{3})|(\d{4}|\d{3})(?:\)))")
pat2 = re.compile(r"((\d{4}|\d{3}) - (\d{4}|\d{3})-(\d{4}|\d{3}))|((?!\d)(\d{4}|\d{3}) - |(\d{4}|\d{3})-(\d{4}|\d{3}) - (\d{4}|\d{3}))")
#
# for x in tests:
#     print(re.findall(pat, x))

multi_years = [
"(English, 1708-1794) (English, 1740-1825) (English, 1740-1825)",
"(Italian, ca. 1445/1450 - 1498/1499)",
"(Dutch, 1508/1509 - 1575)",
"(Dutch, 1588 - 1650/1656)",
"(Dutch, 1533 - before 1578) (Italian, 1540/1541-1609)",
"(Italian, 1680 \u2013 1767) (Italian, 1503\u20131540)",
"(German, 1782 - 1855) (German, 1776-1824)",
"(1480 - 1527-1534)",
"(1480-1527 - 1534)",
"(Italian, ca. 1480 - 1527-1534)"
]

# multi_years.extend(tests)

for x in multi_years:
    x = x.replace(" \u2013 ", "-").replace("\u2013", "-")

    if re.findall(pat2, x):
        print("\nAAAA")
        years = x.split(" - ")
        years = [y.replace("-", "/").strip("(").strip(")") for y in years]
        years[0] = years[0].split(",")[1].strip() if len(years[0].split(",")) > 1 else years[0]

    elif "/" not in x:
        years = re.findall(pat, x)
    elif "/" in x:
        years = re.findall(pat1, x)
        years = [tuple(y for y in tup if y != '') for tup in years]
        years = ["/".join(y) for y in years]


    birth_years = "|".join([years[i] for i in range(0, len(years), 2)])
    death_years = "|".join([years[i] for i in range(1, len(years), 2)])
    # else:
    #     birth_years = years[0]
    #     death_years = "|".join(years[1:])
    # else:
    print("\nString:", x, "\nyears:", years)
    print("Birth:", birth_years, "\ndeath:", death_years)
#
# a = "a - a a-a"
#
# if all([re.findall(r"\s-\s", a), re.findall(r"[^\s]-[^\s]", a)]):
#     print("A")
