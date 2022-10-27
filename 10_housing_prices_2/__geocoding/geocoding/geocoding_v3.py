import csv
import requests
from requests.utils import quote
from tqdm import tqdm
from geopy.geocoders import Nominatim
import json
import yaml
import traceback as tb
from concurrent.futures import ThreadPoolExecutor, as_completed
import heartrate; heartrate.trace(browser=True, daemon=True)
from us_zipcodes import zip_cty_cnty

# geolocator = Nominatim(user_agent="searchtest", domain="127.0.0.1:8088/search.php")
# Validate zipcodes, make sure they are 5 digits and not a range. if range get first.
def zipcode_validator(geocoding):
    try:
        zip5 = geocoding["postcode"]
        if ":" in zip5:
            return zip5.split(":")[0]
        else:
            return zip5
    except KeyError:
        return ""

def geocode(land_info, row, physical_address, city, county, state, writer, url, s):
    save = False

    # Use county and city in the query
    if row["property_county"] and row["property_city"]:
        save = True
        if row["property_zip5"]:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&county={county}&state={state}&postalcode={row["property_zip5"]}&country=US&addressdetails=1&format=jsonv2').text)
        else:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&county={county}&state={state}&country=US&addressdetails=1&format=jsonv2').text)

        if len(response):
            try:
                # Normal response
                geocoding = response["features"][0]["properties"]["geocoding"]
            except TypeError:
                try:
                    # Alternate response
                    geocoding = response[0]["address"]
                except KeyError:
                    # print(str(row["property_street_address"]), "\n")
                    with open("fails.txt", "a") as f:
                        f.write(str(row) + "\n")
                    # tb.print_exc()

            try:
                land_info["property_zip5"] = zipcode_validator(geocoding)
            except UnboundLocalError:
                save = False

    # Use only county in query
    elif not row["property_city"] and row["property_county"]:
        if row["property_zip5"]:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&county={county}&state={state}&postalcode={row["property_zip5"]}country=US&addressdetails=1&format=jsonv2').text)
        else:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&county={county}&state={state}&country=US&addressdetails=1&format=jsonv2').text)

        if len(response):
            save = True
            try:
                geocoding = response["features"][0]["properties"]["geocoding"]
            except TypeError:
                try:
                    geocoding = response[0]["address"]
                except KeyError:
                    # print(str(row["property_street_address"]), "\n")
                    with open("fails.txt", "a") as f:
                        f.write(str(row) + "\n")
                    # print(json.dumps(response, indent=2))
                    # tb.print_exc()

            try:
                land_info["property_zip5"] = zipcode_validator(geocoding)

                # Try to get the city from the response
                if "city" in geocoding.keys():
                    land_info["property_city"] = " ".join(str(geocoding["city"]).upper().split())
                else:
                    try:
                        # Try to get the city based on it's zipcode
                        city = zip_cty_cnty[land_info["property_zip5"]]["city"].upper()
                    except KeyError:
                        pass
            except UnboundLocalError:
                save = False

    # Use only city and not county in query
    elif row["property_city"] and not row["property_county"]:
        if row["property_zip5"]:
                response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&postalcode={row["property_zip5"]}&country=US&addressdetails=1&format=jsonv2').text)
        else:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&addressdetails=1&format=jsonv2').text)

        if len(response):
            save = True
            try:
                geocoding = response["features"][0]["properties"]["geocoding"]
                land_info["property_zip5"] = zipcode_validator(geocoding)
            except TypeError:
                try:
                    geocoding = response[0]["address"]
                except KeyError:
                    # print(str(row["property_street_address"]), "\n")
                    # print(json.dumps(response, indent=2))
                    with open("fails.txt", "a") as f:
                        f.write(str(row) + "\n")
                    # tb.print_exc()

            try:
                land_info["property_zip5"] = zipcode_validator(geocoding)

                # Try to get county from response, otherwise try to get it based on zipcode
                if "property_county" in geocoding.keys():
                    land_info["property_county"] = " ".join(str(geocoding["property_county"]).upper().split())
                else:
                    try:
                        land_info["property_county"] = str(zip_cty_cnty[land_info["property_zip5"]]["property_county"]).upper()
                    except KeyError:
                        pass
            except UnboundLocalError:
                save = False

    # Don't use city or county in query
    elif not row["property_city"] and not row["property_county"]:
        if row["property_zip5"]:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&postalcode={row["property_zip5"]}&country=US&addressdetails=1&format=jsonv2').text)

        else:
            response = json.loads(s.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&addressdetails=1&format=jsonv2').text)

        if len(response):
            save = True
            try:
                geocoding = response["features"][0]["properties"]["geocoding"]
            except TypeError:
                try:
                    geocoding = response[0]["address"]
                except KeyError:
                    # print(str(row["property_street_address"]), "\n")
                    with open("fails.txt", "a") as f:
                        f.write(str(row) + "\n")
                    # print(json.dumps(response, indent=2))
                    # tb.print_exc()

            try:
                land_info["property_zip5"] = zipcode_validator(geocoding)

                # Try to get county and city from response, otherwise try to get it based on zipcode
                if "property_county" in geocoding.keys():
                    land_info["property_county"] = " ".join(str(geocoding["property_county"]).upper().split())
                else:
                    # print("no county 1")
                    try:
                        land_info["property_county"] = str(zip_cty_cnty[land_info["property_zip5"]]["property_county"]).upper()
                    except KeyError:
                        # print("no county")
                        pass

                if "city" in geocoding.keys():
                    land_info["property_city"] = " ".join(str(geocoding["city"]).upper().split())
                else:
                    try:
                        city = str(zip_cty_cnty[land_info["property_zip5"]]["city"]).upper()
                    except KeyError:
                        pass
            except UnboundLocalError:
                save = False

    if save:
        # Verify zip5 one last time
        try:
            if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                land_info["property_zip5"] = ""
        except KeyError:
            pass
            # print(json.dumps(land_info, indent=2))

        writer.writerow(land_info)

def runner(reader, writer, line_count, zip_cty_cnty, columns, url):
    threads = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        s = requests.Session()

        # state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type
        for row in tqdm(reader, total=line_count):
            # Prepare for url format (urlencode didn't work)
            physical_address = str(row["property_street_address"]).replace(" ", "+")
            city = str(row["property_city"]).replace(" ", "+")
            county = str(row["property_county"]).replace(" ", "+")
            state = row["state"]

            # Don't waste time searching for bad addresses
            if len(str(row["property_street_address"])) >= 3:
                land_info = {
                    "state": state,
                    "property_street_address": row["property_street_address"], # Don't fix bad addresses
                    "property_city": " ".join(str(row["property_city"]).upper().split()),
                    "property_county": " ".join(str(row["property_city"]).upper().split()),
                    "sale_datetime": row["sale_datetime"],
                    "sale_price": row["sale_price"],
                    "source_url": row["source_url"].strip(),
                }

                if not row["property_county"] and  "https://portal.assessor.lacounty.gov/" in row["source_url"]:
                    county = "LOS ANGELES"
                    land_info["property_county"] = "LOS ANGELES"


                threads.append(executor.submit(geocode(land_info, row, physical_address, city, county, state, writer, url, s)))

# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
url = "http://127.0.0.1:8088/search.php"
columns = ["state","property_zip5","property_street_address","property_city","property_county","sale_datetime","sale_price","source_url"]

# Load zipcode yaml file into memory
# with open("us_zipcodes.yaml", "r") as f:
#     zip_cty_cnty = yaml.safe_load(f)

# Open source data file
# with open("F:\\us-housing-prices-2\\progresses_zips.csv", "r") as input_csv:
#     # line_count = len([line for line in input_csv.readlines()])
#     line_count = 13855517
#     reader = csv.DictReader(input_csv)
#
#     with open("F:\\us-housing-prices-2\\zip5_added_2.csv", "a", newline="") as output_csv:
#         writer = csv.DictWriter(output_csv, fieldnames=columns)
#         writer.writeheader()
#
#         runner(reader, writer, line_count, zip_cty_cnty, columns, url)


with open("F:\\us-housing-prices-2\\zip5_added_test.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    # line_count = 6433664
    reader = csv.DictReader(input_csv)

    with open("F:\\us-housing-prices-2\\zip5_added_2.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        runner(reader, writer, line_count, zip_cty_cnty, columns, url)
