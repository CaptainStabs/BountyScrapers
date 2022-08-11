import re

a = re.compile(r"((?<=\()(?:\d{3,4})(?=\))|(?<=\()|(?<=\(† )(?:\d{1,2}\.\d{1,2}\.\d{3,4})(?=\)))")

string = ["Dr. Carl Wolf & Sohn (ca. 1847 - nach 1949)",
            "Dr. Carl Wolf & Sohn (ca. 1847-nach 1949)",
            "S.M.S. Hyäne (27.6.1878-1924)"
            ]

for s in string:
    print(re.findall(a, s))
