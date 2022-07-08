import re

dates_pat = re.compile(r"\((.*?)\)")
by_pat = re.compile(r"^By *")
num_only = re.compile(r"[^0-9-]")
names_only = re.compile(r"\([^)]*\)")

string = "By Utagawa Hiroshige (1797-1434)"#, First Last (2134-1241), First1 Last1 (active ca. 1716-1735)"

dates = re.findall(dates_pat, string)[0]

print("Dates:", dates)
for x in dates:
    print("remove letters: ", re.sub(num_only, "", x))
    print()

print("Names:", re.sub(by_pat, "", re.sub(names_only, "", string)))
print("No By:", "".join(re.split(by_pat, string)))

date2 = re.sub(num_only, "", dates)
date2 = date2.split("-")[-1] if len(dates.split("-")) > 1 else None
print("d2",date2)
