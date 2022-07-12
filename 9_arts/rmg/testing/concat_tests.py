
def maker_name(x):
    creator, people = x["creator"], x["people"]
    if creator:
        creator = "|".join(creator.split("; "))
    if people:
        people = "|".join(people.split("; "))
    l = [x for x in [creator, people] if x]
    if len(l):
        return "|".join(l)
    else:
        return

x = [
    {"creator": "creator", "people": "people"},
    {"creator": None, "people": "Last, first name; last1, first1"},
    {"creator": "Creator1, Creatorlast1; creator2", "people": "Last, first name; last1, first1"}
]

for i, y in enumerate(x):
    print(f"{i}:", maker_name(y))
