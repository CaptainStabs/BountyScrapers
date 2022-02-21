
with open("_data_fields.txt", "r") as f:

    fields = []
    for line in f.readlines():
        fields.append(line.split(" ( ")[0])

print(fields)
