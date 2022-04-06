import re
#
# c = '0D160JA-0D160JL'
# p = re.compile('\d[a-zA-Z]+\d\d\d[a-zA-Z][a-zA-Z0-9]')
#
# if "-" in c.strip("-") and not bool(p.search(c.split("-")[0].strip())):
#     print("TRUE")
#
# print(bool(p.search(c.split("-")[0].strip())))
#
# if not bool(p.search(c.split("-")[0].strip())):
#     print("A")

c = "030-123"
p = re.compile('([A-TV-Z][0-9][A-Z0-9](\.?[A-Z0-9]{0,4})?)')
print(p.search(c))
