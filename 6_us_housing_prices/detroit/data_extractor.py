import csv
from dateutil import parser
from tqdm import tqdm

columns = ["state", "physical_address", "sale_date", "book", "page"]
with open("Property_Sales.csv", 'r') as f:
    read_csv = csv.reader(f)

    with open("extracted.csv", "a") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        for i, row in tqdm(enumerate(read_csv)):
            try:
                del book
                del page
            except:
                pass

            if i:
                if row[6]:
                    land_info = {
                        "state": "MI",
                        "physical_address": row[2],
                        "sale_date": str(parser.parse(str(row[4])))[:-6]
                    }


                    book = row[6]

                    try:
                        if "/" not in book:
                            if "LIBER" in book:
                                # print(book)
                                book = row[6].split("PAGE")[0].replace("LIBER ", "").strip()
                                page = row[6].split("PAGE")[1].strip().lstrip(":").lstrip("P:").lstrip("P").strip()


                            elif "L:" and "P:" in book:
                                book = str(row[6].split("P:")[0]).lstrip("L:").strip()
                                page = row[6].split("P:")[1].lstrip(":").lstrip("P:").lstrip("P").strip()

                            elif ", " in book:
                                book = str(row[6].split(", ")[0]).lstrip("L").rstrip(",").strip()
                                page = str(row[6].split(", ")[1]).lstrip("P").lstrip(":").strip()

                            elif ":" in book:
                                book = row[6].split(":")[0].strip().lstrip("L").lstrip(":").lstrip("L:").strip()
                                page = row[6].split(":")[1].lstrip(":").lstrip("P:").lstrip("P").strip()

                            elif "-" in book:
                                book = row[6].split("-")[0].lstrip("L").lstrip(":").lstrip("L:").strip()
                                page = row[6].split("-")[1].lstrip(":").lstrip("P:").lstrip("P").strip()

                            elif ";" in book:
                                book = row[6].split(";")[0].lstrip("L").lstrip(":").lstrip("L:").strip()
                                page = row[6].split(";")[1].lstrip(":").lstrip("P:").lstrip("P").strip()


                            elif "L" and "P" in book:
                                book = str(row[6].split("P")[0]).lstrip("L").strip()
                                page = str(row[6].split("P")[1]).lstrip(":").lstrip("P:").strip()

                            elif " " in book:
                                book = row[6].split(" ")[0].lstrip("L").strip()
                                page = row[6].split(" ")[1].lstrip("P").lstrip(":").lstrip("P:").strip()



                            # else:
                            #     if len(row[6]) != 10:
                            #         print(row[6])
                        elif "/" in book:
                            book = row[6].split("/")[0].strip().lstrip("L").lstrip(":").lstrip("L:").strip()

                            try:
                                page = row[6].split("/")[1].strip().lstrip("P").lstrip(":").lstrip("P:").strip()
                            except IndexError:
                                pass
                                print(row[6])
                        else:
                            print(row[6])

                        try:
                            if "-" in page:
                                page = page.split("-")[0]

                            land_info["book"] = book
                            land_info["page"] = page
                            writer.writerow(land_info)

                        except NameError:
                            pass
                            # if len(row[6]) != 10:
                            #     print(row[6])
                    except IndexError:
                        print(book)
