import csv
import requests
from requests.utils import quote
from tqdm import tqdm
from geopy.geocoders import Nominatim
import json
import yaml
import traceback as tb

# geolocator = Nominatim(user_agent="searchtest", domain="127.0.0.1:8088/search.php")

def zipcode_validator(geocoding):
    try:
        zip5 = geocoding["postcode"]
        if ":" in zip5:
            return zip5.split(":")[0]
        else:
            return zip5
    except KeyError:
        return ""

# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
url = "http://127.0.0.1:8088/search.php"
columns = ["state","zip5","physical_address","city","county","property_id","sale_date","property_type","sale_price","seller_name","buyer_name","num_units","year_built","source_url","book","page","sale_type"]

with open("us_zipcodes.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)

with open("F:\\us-housing-prices-2\\null_zips.csv", "r") as input_csv:
    # line_count = len([line for line in input_csv.readlines()])
    line_count = 20550428
    reader = csv.DictReader(input_csv)

    with open("F:\\us-housing-prices-2\\zip5_added.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

    # state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type
        for row in tqdm(reader, total=line_count):
            save = False
            physical_address = str(row["physical_address"]).replace(" ", "+")
            city = str(row["city"]).replace(" ", "+")
            county = str(row["county"]).replace(" ", "+")
            state = row["state"]

            if len(str(row["physical_address"])) > 3:
                land_info = {
                    "state": row["state"],
                    "physical_address": row["physical_address"],
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
                    # "zip5": row["zip5"],
                    # "city": " ".join(str(row["city"]).split()).strip(),
                    # "county": " ".join(str(row["county"]).split()).strip(),

                if not land_info["book"] or not land_info["page"]:
                    land_info["book"] = ""
                    land_info["page"] = ""

                # query = url+"?q=" + requests.utils.quote(f"{physical_address},{city},{county},{state},US")
                # query = url + "?q=" + str(f"{physical_address},{city},{county},{state},US")
                # print(query)
                #
                # print(requests.request("GET", query).text)
                if row["county"] and row["city"]:
                    save = True
                    response = json.loads(requests.request("GET", f'{url}?street={physical_address}&city={city}&county={county}&state={state}&country=US&addressdetails=1&format=jsonv2').text)
                    if len(response):
                        try:
                            geocoding = response["features"][0]["properties"]["geocoding"]
                        except TypeError:
                            try:
                                geocoding = response[0]["address"]
                            except KeyError:
                                # print(str(row["physical_address"]), "\n")
                                with open("fails.txt", "a") as f:
                                    f.write(str(row) + "\n")
                                # tb.print_exc()

                        land_info["zip5"] = zipcode_validator(geocoding)
                elif row["county"] and not row["city"]:
                    response = json.loads(requests.request("GET", f'{url}?street={physical_address}&county={county}&state={state}&country=US&addressdetails=1&format=jsonv2').text)
                    if len(response):
                        save = True
                        try:
                            geocoding = response["features"][0]["properties"]["geocoding"]
                        except TypeError:
                            try:
                                geocoding = response[0]["address"]
                            except KeyError:
                                # print(str(row["physical_address"]), "\n")
                                with open("fails.txt", "a") as f:
                                    f.write(str(row) + "\n")
                                # print(json.dumps(response, indent=2))
                                # tb.print_exc()

                        land_info["zip5"] = zipcode_validator(geocoding)
                        if "city" in geocoding.keys():
                            land_info["city"] = " ".join(str(geocoding["city"]).upper().split())
                        else:
                            try:
                                city = zip_cty_cnty[land_info["zip5"]]["city"].upper()
                            except KeyError:
                                pass


                elif row["city"] and not row["county"]:
                    response = json.loads(requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&addressdetails=1&format=jsonv2').text)
                    if len(response):
                        save = True
                        try:
                            geocoding = response["features"][0]["properties"]["geocoding"]
                            land_info["zip5"] = zipcode_validator(geocoding)
                        except TypeError:
                            try:
                                geocoding = response[0]["address"]
                            except KeyError:
                                # print(str(row["physical_address"]), "\n")
                                # print(json.dumps(response, indent=2))
                                with open("fails.txt", "a") as f:
                                    f.write(str(row) + "\n")
                                # tb.print_exc()

                        land_info["zip5"] = zipcode_validator(geocoding)

                        if "county" in geocoding.keys():
                            land_info["county"] = " ".join(str(geocoding["county"]).upper().split())
                        else:
                            try:
                                land_info["county"] = str(zip_cty_cnty[land_info["zip5"]]["county"]).upper()
                            except KeyError:
                                pass

                elif not row["city"] and not row["county"]:
                    response = json.loads(requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&addressdetails=1&format=jsonv2').text)
                    if len(response):
                        save = True
                        try:
                            geocoding = response["features"][0]["properties"]["geocoding"]
                        except TypeError:
                            try:
                                geocoding = response[0]["address"]
                            except KeyError:
                                # print(str(row["physical_address"]), "\n")
                                with open("fails.txt", "a") as f:
                                    f.write(str(row) + "\n")
                                # print(json.dumps(response, indent=2))
                                # tb.print_exc()

                        land_info["zip5"] = zipcode_validator(geocoding)

                        if "county" in geocoding.keys():
                            land_info["county"] = " ".join(str(geocoding["county"]).upper().split())
                        else:
                            try:
                                land_info["county"] = str(zip_cty_cnty[land_info["zip5"]]["county"]).upper()
                            except KeyError:
                                pass

                        if "city" in geocoding.keys():
                            land_info["city"] = " ".join(str(geocoding["city"]).upper().split())
                        else:
                            try:
                                city = str(zip_cty_cnty[land_info["zip5"]]["city"]).upper()
                            except KeyError:
                                pass

                if save:
                    try:
                        if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                            land_info["zip5"] = ""
                    except KeyError:
                        pass
                        # print(json.dumps(land_info, indent=2))

                    writer.writerow(land_info)

                # print(json.dumps(json.JSONDecoder().decode(response.text), indent=2))
                # print(response.json)
                # print(response.text)
                # print(response.content)
                # print(location)
                # break
