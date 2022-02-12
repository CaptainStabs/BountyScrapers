import csv
import requests
from requests.utils import quote
from tqdm import tqdm
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="searchtest")


# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
# url = "https://nominatim.openstreetmap.org/search?"

with open("test.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

# state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type
    for row in reader:
        # physical_address = str(row["physical_address"]).replace(" ", "+")
        # city = str(row["city"]).replace(" ", "+")
        # county = str(row["county"]).replace(" ", "+")
        # state = row["state"]


        location = geolocator.geocode(address)
        print(location)
        # query = url+"?q=" + requests.utils.quote(f"{physical_address},{city},{county},{state},US")
        print(query)

        if row["county"] and row["city"]:
            address = ", ".join([str(row["physical_address"]), str(row["city"]), row["county"], row["state"]])

        elif row["county"] and not row["city"]:
            address = ", ".join([str(row["physical_address"]), row["county"], row["state"]])

        elif row["city"] and not row["county"]:
            address = ", ".join([str(row["physical_address"]), str(row["city"]), row["state"]])

        elif not row["city"] and not row["county"]:
            address = ", ".join([str(row["physical_address"]), row["state"]])

        response = requests.request("GET", query, headers=headers)
        print(response.json)
        print(response.text)
        print(response.content)
        break
