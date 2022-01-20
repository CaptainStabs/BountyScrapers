import csv
from tqdm import tqdm

columns = ["property_id", "num_units", "physical_address", "sale_date", "sale_price", "book", "page", "year_built", "zip5", "state", "county", "city", "source_url"]
with open("extracted_data.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("fixed_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader):
            land_info = {
                "property_id": row["property_id"].strip(),
                "num_units": row["num_units"],
                "physical_address": row["physical_address"].strip(),
                "sale_price": row["sale_price"],
                "book": row["book"].replace("DB", "").replace("A", ""),
                "page": row["page"].split(".")[0],
                "year_built": row["year_built"],
                "zip5": row["zip5"],
                "state": row["state"].strip(),
                "county": row["county"].strip(),
                "city": row["city"],
                "source_url": row["source_url"],
            }
            try:
                if int(land_info["book"]) <= 0:
                    land_info["book"] = ""
            except:
                land_info["book"] = ""
                continue

            if row["book"] == "0000":
                land_info["book"] = ""

            if row["page"] == "0000":
                land_info["page"] = ""

            try:
                if int(land_info["page"]) <= 0:
                    land_info["page"] = ""

            except:
                land_info["page"] = ""
                continue

            try:
                if land_info["book"] and not land_info["page"]:
                    land_info["book"] = ""
                elif land_info["page"] and not land_info["book"]:
                    land_info["page"] = ""

            except KeyError:
                continue

            try:
                sale_date = str(row["sale_date"])
                year = sale_date.split("-")[0]

                if int(year) > 2022:
                    year = sale_date.split("-")[0]
                    sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                    land_info["sale_date"] = sale_date
                elif int(year) == 2022:
                    if int(sale_date.split("-")[1]) > 2:
                        sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                        land_info["sale_date"] = sale_date

                else:
                    land_info["sale_date"] = row["sale_date"]

                # if int(land_info["sale_date"].split("-")[0]) > 1492:
                if land_info["sale_date"]:
                    writer.writerow(land_info)

            except ValueError:
                print(row["sale_date"])

            except KeyError:
                # print(land_info)
                continue
