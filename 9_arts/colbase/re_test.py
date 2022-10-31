import re

by_pat = re.compile(r"^By *")
remove_escaped = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
dates_pat = re.compile(r"\((.*?)\)")
by_pat = re.compile(r"^By *")
num_only = re.compile(r"[^0-9-]")
names_only = re.compile(r"\([^)]*\)")
delims = ["and", ",",";"]

sakusha = "By Utagawa Hiroshige (1797-1858)"
names = "|".join(re.split(re.compile(r"( and |, |;)"), re.sub(by_pat, "", re.sub(names_only, "",  sakusha)))).replace("Compiled by", "").replace("illustrated by", "").replace("Illustrated by", "") .replace("illustrated by", "")if sakusha else None
print(names)
