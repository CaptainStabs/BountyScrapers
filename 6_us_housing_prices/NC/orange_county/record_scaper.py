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

land_info = {
    "state":"NC"
}

print(json.dumps(json_data, indent=2))
