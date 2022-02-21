filename = "all_fields.txt"
f = open(filename, "r")
fields = []
exclude_list = ["SALE", "GRANTOR", "GRANTEE", "ASSESS", "MAIL", "BOOK", "PAGE", "ADDR"]
with open("fields.txt", "r") as f:
    for line in f.readlines():
        line2 = line.replace('"', "").upper().strip().replace(" ", "_")
        if line2 not in fields and not any(x in line2 for x in exclude_list):
            fields.append(line2)

with open("fields2.txt", "a") as save_fields:
    for field in fields:
        save_fields.write(f"{field}\n")
