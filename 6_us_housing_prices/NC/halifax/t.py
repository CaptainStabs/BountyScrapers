
row = {"BK_PG": "0/52"}

book = row["BK_PG"].split("/")[0].strip()
page = row["BK_PG"].split("/")[1].strip()

if book != "0":
    print(book)
