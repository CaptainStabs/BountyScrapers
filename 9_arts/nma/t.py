a = {   "type": "Measurement",
    "height": 540,
    "width": 670,
    "unitText": "mm"
}

units = list(a.values())[1:-1]
print(units)
# b = [x[y for y in units] for x in a]


# print(b)
print(list(a.keys())[1:-1])
