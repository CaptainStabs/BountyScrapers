import csv
from tqdm import tqdm
columns = ["state", "zip5", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]
columns2 = ["state", "zip5", "physical_address","county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]
columns3 = ["state", "zip5", "physical_address","city", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]
columns4 = ["state", "zip5", "physical_address", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]

with open("F:\\us-housing-prices-2\\zip5_added_test.csv") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("F:\\us-housing-prices-2\\clean\\cities_counties_fixed.csv", "a") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        with open("F:\\us-housing-prices-2\\clean\\counties_fixed.csv", "a") as output_csv2:
            writer2 = csv.DictWriter(output_csv2, fieldnames=columns2)
            writer2.writeheader()

            with open("F:\\us-housing-prices-2\\clean\\cities_fixed.csv", "a") as output_csv3:
                writer3 = csv.DictWriter(output_csv3, fieldnames=columns3)
                writer3.writeheader()

                with open("F:\\us-housing-prices-2\\clean\\zips_fixed.csv", "a") as output_csv4:
                    writer4 = csv.DictWriter(output_csv4, fieldnames=columns4)
                    writer4.writeheader()


                    for row in tqdm(reader):
                        land_info = {}
                        if row["city"] and row["county"]:
                            land_info = {
                                "state": row["state"],
                                "physical_address": row["physical_address"], # Don't fix bad addresses
                                "zip5": row["zip5"],
                                "city": " ".join(str(row["city"]).upper().split()),
                                "county": " ".join(str(row["city"]).upper().split()),
                                "property_id": row["property_id"].strip(),
                                "sale_date": row["sale_date"],
                                "property_type": " ".join(str(row["property_type"]).upper().split()),
                                "sale_price": row["sale_price"],
                                "seller_name": " ".join(str(row["seller_name"]).split()).strip().strip(),
                                "buyer_name": " ".join(str(row["buyer_name"]).split()).strip().strip(),
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"].strip(),
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"].strip(),
                            }

                            year = land_info["sale_date"].split("-")[0]
                            month = land_info["sale_date"].split("-")[1]
                            try:
                                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                                    land_info["zip5"] = ""
                            except KeyError:
                                pass

                            try:
                                int(land_info["zip5"])
                            except ValueError:
                                land_info["zip5"] = ""
                            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) < 2022:
                                if int(year) == 2022:
                                    if int(month) <= 2:
                                        writer.writerow(land_info)
                                else:
                                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                                        writer.writerow(land_info)
                            writer.writerow(land_info)

                        elif row["county"] and not row["city"]:
                            land_info = {
                                "state": row["state"],
                                "physical_address": row["physical_address"], # Don't fix bad addresses
                                "zip5": row["zip5"],
                                # "city": " ".join(str(row["city"]).upper().split()),
                                "county": " ".join(str(row["city"]).upper().split()),
                                "property_id": row["property_id"].strip(),
                                "sale_date": row["sale_date"],
                                "property_type": " ".join(str(row["property_type"]).upper().split()),
                                "sale_price": row["sale_price"],
                                "seller_name": " ".join(str(row["seller_name"]).split()).strip().strip(),
                                "buyer_name": " ".join(str(row["buyer_name"]).split()).strip().strip(),
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"].strip(),
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"].strip(),
                            }


                            year = land_info["sale_date"].split("-")[0]
                            month = land_info["sale_date"].split("-")[1]
                            try:
                                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                                    land_info["zip5"] = ""
                            except KeyError:
                                pass

                            try:
                                int(land_info["zip5"])
                            except ValueError:
                                land_info["zip5"] = ""

                            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) < 2022:
                                if int(year) == 2022:
                                    if int(month) <= 2:
                                        writer2.writerow(land_info)
                                else:
                                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                                        writer2.writerow(land_info)

                        elif row["city"] and not row["county"]:
                            land_info = {
                                "state": row["state"],
                                "physical_address": row["physical_address"], # Don't fix bad addresses
                                "zip5": row["zip5"],
                                "city": " ".join(str(row["city"]).upper().split()),
                                # "county": " ".join(str(row["city"]).upper().split()),
                                "property_id": row["property_id"].strip(),
                                "sale_date": row["sale_date"],
                                "property_type": " ".join(str(row["property_type"]).upper().split()),
                                "sale_price": row["sale_price"],
                                "seller_name": " ".join(str(row["seller_name"]).split()).strip().strip(),
                                "buyer_name": " ".join(str(row["buyer_name"]).split()).strip().strip(),
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"].strip(),
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"].strip(),
                            }
                            try:
                                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                                    land_info["zip5"] = ""
                            except KeyError:
                                pass

                            try:
                                int(land_info["zip5"])
                            except ValueError:
                                land_info["zip5"] = ""

                            year = land_info["sale_date"].split("-")[0]
                            month = land_info["sale_date"].split("-")[1]
                            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) < 2022:
                                if int(year) == 2022:
                                    if int(month) <= 2:
                                        writer3.writerow(land_info)
                                else:
                                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                                        writer3.writerow(land_info)

                        elif not row["city"] and not row["county"]:
                            land_info = {
                                "state": row["state"],
                                "physical_address": row["physical_address"], # Don't fix bad addresses
                                "zip5": row["zip5"],
                                # "city": " ".join(str(row["city"]).upper().split()),
                                # "county": " ".join(str(row["city"]).upper().split()),
                                "property_id": row["property_id"].strip(),
                                "sale_date": row["sale_date"],
                                "property_type": " ".join(str(row["property_type"]).upper().split()),
                                "sale_price": row["sale_price"],
                                "seller_name": " ".join(str(row["seller_name"]).split()).strip().strip(),
                                "buyer_name": " ".join(str(row["buyer_name"]).split()).strip().strip(),
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"].strip(),
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"].strip(),
                            }
                            try:
                                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                                    land_info["zip5"] = ""
                            except KeyError:
                                pass

                            try:
                                int(land_info["zip5"])
                            except ValueError:
                                land_info["zip5"] = ""
                                
                            year = land_info["sale_date"].split("-")[0]
                            month = land_info["sale_date"].split("-")[1]
                            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) < 2022:
                                if int(year) == 2022:
                                    if int(month) <= 2:
                                        writer4.writerow(land_info)
                                else:
                                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                                        writer4.writerow(land_info)
