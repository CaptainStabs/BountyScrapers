import csv
from tqdm import tqdm
import datetime
import traceback as tb

# ''GPN', ' 'SitusAddress', 'SitusCity', 'SitusZip','ClassValue', ,  '', 'RecorderLink', '',
# 'TaxSale1DateSale', '', 'TaxSale1BuyerAmount', '', 'TaxSale2DateSale', '', 'TaxSale2BuyerAmount', '', 'TaxSale3DateSale', 'TaxSale3DateRedemption', 'TaxSale3BuyerAmount', 'TaxSale4Certificate', 'TaxSale4DateSale', 'TaxSale4DateRedemption', 'TaxSale4BuyerAmount', 'TaxSale5Certificate', 'TaxSale5DateSale', 'TaxSale5DateRedemption', 'TaxSale5BuyerAmount',
columns = ["property_id", "physical_address", "city", "zip5", "property_type", "sale_date", "sale_price", "book", "page", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["GPN"],
                    "physical_address": " ".join(str(row["SitusAddress"]).upper().split()),
                    "city": " ".join(str(row["SitusCity"]).upper().split()),
                    "zip5": row["SitusZip"],
                    "property_type": " ".join(str(row["ClassValue"]).upper().split()),
                    "county": "LINN",
                    "state": "IA",
                    "source_url": row["RecorderLink"]
                }
                # &bk=9826&pg=600&idx=GEN

                # Delete if no book
                # Update field
                try:
                    if "&bk=&pg=&" not in row["RecorderLink"] and row["RecorderLink"]:
                        bk_index = row["RecorderLink"].split("&pg=")[0].index("&bk=")
                        book = str(row["RecorderLink"].split("&pg=")[0][bk_index:].replace("&bk=", "")).strip()
                        page = str(row["RecorderLink"].split("&pg=")[1].replace("&idx=GEN", "")).strip()

                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                except ValueError as e:
                    # tb.print_exc()
                    # print(row["RecorderLink"])
                    pass

                except IndexError:
                    pass

                # Delete if no year_built
                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                for i in range(1,6):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        timestamp = int(row[f"TaxSale{i}DateSale"])
                        land_info["sale_date"] = datetime.datetime.fromtimestamp((timestamp/1000))
                        land_info["sale_price"] = row[f"TaxSale{i}BuyerAmount"]
                    except ValueError as e:
                        # print(e)
                        pass
                    try:
                        year = land_info["sale_date"].year

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)
                    except KeyError:
                        pass

            except Exception as e:
                raise e
                pass
