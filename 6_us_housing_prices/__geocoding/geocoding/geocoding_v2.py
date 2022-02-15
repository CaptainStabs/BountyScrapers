import csv
import requests
from requests.utils import quote
from tqdm import tqdm
from geopy.geocoders import Nominatim
import json
# geolocator = Nominatim(user_agent="searchtest", domain="127.0.0.1:8088/search.php")


# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
url = "http://127.0.0.1:8088/search.php"

with open("test.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

# state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type
    for row in tqdm(reader, total=line_count):
        physical_address = str(row["physical_address"]).replace(" ", "+")
        city = str(row["city"]).replace(" ", "+")
        county = str(row["county"]).replace(" ", "+")
        state = row["state"]



        # query = url+"?q=" + requests.utils.quote(f"{physical_address},{city},{county},{state},US")
        # query = url + "?q=" + str(f"{physical_address},{city},{county},{state},US")
        # print(query)
        #
        # print(requests.request("GET", query).text)
        if row["county"] and row["city"]:
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&county={county}&state={state}&country=US&format=jsonv2')

        elif row["county"] and not row["city"]:
            response = requests.request("GET", f'{url}?street={physical_address}&county={county}&state={state}&country=US&format=jsonv2')

        elif row["city"] and not row["county"]:
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&format=jsonv2')

        elif not row["city"] and not row["county"]:
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US&format=jsonv2')

        land_info = {
            "state": row["state"],
            "zip5": row["zip5"],
            "physical_address": row["physical_address"],
            "city": " ".join(str(row["city"]).split()).strip(),
            "county": " ".join(str(row["county"]).split()).strip(),
            "property_id": row["property_id"].strip(),
            "sale_date": row["sale_date"],
            "property_type": row["property_type"].strip(),
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
        print(json.dumps(json.JSONDecoder().decode(response.text), indent=2))
        # print(response.json)
        # print(response.text)
        # print(response.content)
        # print(location)
        break
