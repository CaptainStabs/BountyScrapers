import csv
from dateutil import parser
from tqdm import tqdm

columns = ["state", "physical_address", "sale_date", "book", "page"]
with open("Property_Sales.csv", 'r') as f:
    read_csv = csv.reader(f)

    with open("extracted.csv", "a") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        for i, row in tqdm(enumerate(read_csv)):
            if i:
                if row[6]:
                    land_info = {
                        "state": "MI",
                        "physical_address": row[2],
                        "sale_date": str(parser.parse(str(row[4])))[:-6]
                    }

                    book = row[6]

                    if "/" not in book:
                        if " " in book:
                            book = row[6].split(" ")[0].lstrip("L")
                            page = row[6].split(" ")[1].lstrip("P")
                        elif ":" in book:
                            book = row[6].split(":")[0]
                            page = row[6].split(":")[1]

                        elif "-" in book:
                            book = row[6].split("-")[0]
                            page = row[6].split("-")[1]

                        elif ";" in book:
                            book = row[6].split(";")[0]
                            page = row[6].split(";")[1]

                        elif "L" and "P" in book:
                            book = str(row[6].split("P")[0]).lstrip("L")
                            page = str(row[6].split("P")[1])

                        elif ", " in book:
                            book = str(row[6].split(", ")[0]).lstrip("L")
                            page = str(row[6].split(", ")[1]).lstrip("P")

                        # else:
                        #     if len(row[6]) != 10:
                        #         print(row[6])
                    else:
                        try:
                            page = row[6].split("/")[1]
                        except IndexError:
                            pass
                            # print(row[6])

                    if "-" in page:
                        page = page.split("-")[0]
                    land_info["book"] = book
                    land_info["page"] = page
                    writer.writerow(land_info)
