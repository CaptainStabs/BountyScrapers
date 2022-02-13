import yaml
import csv
from tqdm import tqdm
import json
# import heartrate; heartrate.trace(browser=True)

columns = ["state", "zip5", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url", "book", "page", "sale_type"]
removed_zips = []
wrong_state = {}
with open("us_zipcodes.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)
    # print(zip_cty_cnty[31419])

with open("F:\\us-housing-prices-2\\null_counties.csv", "r") as input_csv:
    line_count = 3489716 #len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("F:\\us-housing-prices-2\\added_counties.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            success = False
            zip_error = False
            if row["zip5"] and row["city"]:
                try:
                    county = zip_cty_cnty[row["zip5"]]["county"]
                    city = zip_cty_cnty[row["zip5"]]["city"]
                    state = zip_cty_cnty[row["zip5"]]["state"]
                except KeyError:
                    try:
                        county = zip_cty_cnty[str(int(row["zip5"])+1)]["county"]
                        city = zip_cty_cnty[str(int(row["zip5"])+1)]["city"]
                        state = zip_cty_cnty[str(int(row["zip5"])+1)]["state"]
                    except KeyError:
                        try:
                            county = zip_cty_cnty[str(int(row["zip5"])-1)]["county"]
                            city = zip_cty_cnty[str(int(row["zip5"])-1)]["city"]
                            state = zip_cty_cnty[str(int(row["zip5"])-1)]["state"]
                        except KeyError:
                            zip_error = True
                            # print(row["zip5"])

                if not zip_error:
                    if state == row["state"]:
                        land_info = {
                            "state": row["state"],
                            "zip5": row["zip5"],
                            "physical_address": row["physical_address"],
                            "city": row["city"],
                            "county": str(county).upper().strip(),
                            "property_id": row["property_id"],
                            "sale_date": row["sale_date"],
                            "sale_price": row["sale_price"],
                            "seller_name": row["seller_name"],
                            "buyer_name": row["buyer_name"],
                            "num_units": row["num_units"],
                            "year_built": row["year_built"],
                            "source_url": row["source_url"],
                            "book": row["book"],
                            "page": row["page"],
                            "sale_type": row["sale_type"]
                        }
                    else:
                        land_info = {
                            "state": row["state"],
                            "zip5": "",
                            "physical_address": row["physical_address"],
                            "city": row["city"],
                            "county": "",
                            "property_id": row["property_id"],
                            "sale_date": row["sale_date"],
                            "sale_price": row["sale_price"],
                            "seller_name": row["seller_name"],
                            "buyer_name": row["buyer_name"],
                            "num_units": row["num_units"],
                            "year_built": row["year_built"],
                            "source_url": row["source_url"],
                            "book": row["book"],
                            "page": row["page"],
                            "sale_type": row["sale_type"]
                            }

                        if row["zip5"] not in wrong_state.keys():
                            wrong_state[row["zip5"]] = row["source_url"]

                    success = True

                else:
                    success = True
                    land_info = {
                        "state": row["state"],
                        "zip5": "",
                        "physical_address": row["physical_address"],
                        "city": row["city"],
                        "county": "",
                        "property_id": row["property_id"],
                        "sale_date": row["sale_date"],
                        "sale_price": row["sale_price"],
                        "seller_name": row["seller_name"],
                        "buyer_name": row["buyer_name"],
                        "num_units": row["num_units"],
                        "year_built": row["year_built"],
                        "source_url": row["source_url"],
                        "book": row["book"],
                        "page": row["page"],
                        "sale_type": row["sale_type"]
                    }

            elif row["zip5"] and not row["city"]:
                try:
                    county = zip_cty_cnty[row["zip5"]]["county"]
                    city = zip_cty_cnty[row["zip5"]]["city"]
                    state = zip_cty_cnty[row["zip5"]]["state"]
                except KeyError:
                    try:
                        county = zip_cty_cnty[str(int(row["zip5"])+1)]["county"]
                        city = zip_cty_cnty[str(int(row["zip5"])+1)]["city"]
                        state = zip_cty_cnty[str(int(row["zip5"])+1)]["state"]
                    except KeyError:
                        try:
                            county = zip_cty_cnty[str(int(row["zip5"])-1)]["county"]
                            city = zip_cty_cnty[str(int(row["zip5"])-1)]["city"]
                            state = zip_cty_cnty[str(int(row["zip5"])-1)]["state"]
                        except KeyError:
                            # print(row["zip5"])
                            zip_error = True

                    if not zip_error:
                        if state == row["state"]:
                            land_info = {
                                "state": row["state"],
                                "zip5": row["zip5"],
                                "physical_address": row["physical_address"],
                                "city": str(city).upper().strip(),
                                "county": str(county).upper().strip(),
                                "property_id": row["property_id"],
                                "sale_date": row["sale_date"],
                                "sale_price": row["sale_price"],
                                "seller_name": row["seller_name"],
                                "buyer_name": row["buyer_name"],
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"],
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"]
                            }
                        else:
                            land_info = {
                                "state": row["state"],
                                "zip5": "",
                                "physical_address": row["physical_address"],
                                "city": "",
                                "county": "",
                                "property_id": row["property_id"],
                                "sale_date": row["sale_date"],
                                "sale_price": row["sale_price"],
                                "seller_name": row["seller_name"],
                                "buyer_name": row["buyer_name"],
                                "num_units": row["num_units"],
                                "year_built": row["year_built"],
                                "source_url": row["source_url"],
                                "book": row["book"],
                                "page": row["page"],
                                "sale_type": row["sale_type"]
                            }
                            if row["zip5"] not in wrong_state.keys():
                                wrong_state[row["zip5"]] = row["source_url"]
                        success = True
                    else:
                        success = True
                        land_info = {
                            "state": row["state"],
                            "zip5": "",
                            "physical_address": row["physical_address"],
                            "city": "",
                            "county": "",
                            "property_id": row["property_id"],
                            "sale_date": row["sale_date"],
                            "sale_price": row["sale_price"],
                            "seller_name": row["seller_name"],
                            "buyer_name": row["buyer_name"],
                            "num_units": row["num_units"],
                            "year_built": row["year_built"],
                            "source_url": row["source_url"],
                            "book": row["book"],
                            "page": row["page"],
                            "sale_type": row["sale_type"]
                        }

            if zip_error:
                if row["zip5"] not in removed_zips:
                    removed_zips.append(row["zip5"])

            if success:
                writer.writerow(land_info)
            # if zip_error:
            #     break

print(removed_zips)
print("")
print(json.dumps(wrong_state, indent=2))
