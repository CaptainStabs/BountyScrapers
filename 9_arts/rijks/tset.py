def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

lst = [{'id':'1234','name':'Tom'}, {'id':'2345','name':'Tom'}, {'id':'3456','name':'Art'}]

pbn = build_dict(lst, key="name")
print(pbn.get("Tom"))
