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
print("d1",date2.split("-")[0])
date2 = date2.split("-")[-1] if len(dates.split("-")) > 1 else None
print("d2",date2)

a = "By Utagawa Hirsohiga and this, that; is"

names = "|".join(re.split(re.compile(r"(and|, |;)"), re.sub(by_pat, "", re.sub(names_only, "", a)))).replace("Compiled by", "").replace("illustrated by", "").replace("Illustrated by", "")
delims = ["and", ",",";"]
print("|".join([x for x in [x.strip() if not any(delims in x for delims in delims) else "" for x in names.split("|") ] if x.strip()]))
