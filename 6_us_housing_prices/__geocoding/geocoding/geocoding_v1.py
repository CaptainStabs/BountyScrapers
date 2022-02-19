import csv
import requests
from tqdm import tqdm

headers = {"user-agent": "zipcode_geocoder"}
url = "https://nominatim.openstreetmap.org/search?"

with open("test.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

# state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type
    for row in reader:
        physical_address = str(row["physical_address"]).replace(" ", "+")
        city = str(row["city"]).replace(" ", "+")
        county = str(row["county"]).replace(" ", "+")
        state = row["state"]
        # print(url+"?q=" + requests.utils.quote(f"{physical_address},{city},{county},{state},US"))
        #
        if row["county"] and row["city"]:
            query = 
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&county={county}&state={state}&country=US')

        elif row["county"] and not row["city"]:
            response = requests.request("GET", f'{url}?street={physical_address}&county={county}&state={state}&country=US')

        elif row["city"] and not row["county"]:
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US')

        elif not row["city"] and not row["county"]:
            response = requests.request("GET", f'{url}?street={physical_address}&city={city}&state={state}&country=US')

        print(response.json)
        print(response.text)
        print(response.content)
        break
