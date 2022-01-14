import csv
from tqdm import tqdm
import os
from dateutil import parser
import json
import requests

url = "https://property.spatialest.com/nc/orange/api/v1/recordcard/9990956954"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
cleaned_response = str(response.text).replace("\\", "").strip('"')
json_data = json.loads(cleaned_response)

sale_data = parcel["sections"][3][0][0]

land_info = {
    "state": "NC",
    "county": "ORANGE COUNTY",
    "sale_date": sale_data["order_0"],
    "book": sale_data["Book"],
    "page": sale_data["Page"],

}

if sale_data["seller_name"] != "null":
    land_info["seller_name"] = sale_data["seller_name"]

if sale_data["SalePrice"] != "null":
    # save
    land_info["sale_price"] = sale_data["SalePrice"]

parcel = json_data["parcel"]
sale_date = parcel["sections"][3][0][0]["order_0"]
# print(json.dumps(json_data, indent=2))
print(sale_date)
