import requests
import jmespath
import json
from dateutil import parser

url = "https://property.spatialest.com/nc/durham/data/propertycard"


headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'XSRF-TOKEN=eyJpdiI6IjA4cHFaaytiT1kxWVNPN1VPcWhRQ1E9PSIsInZhbHVlIjoiN1VIK0hlc1BabXpIbkFMVVpKRENlUzBmaThSZHFFUzF6ZTJZdUMwTWwwK3E1anUrakV2UkhqZEdXbFhtMEoraCIsIm1hYyI6ImZjODQ1M2YxYTdkZmJkYjU1YzZjMTYzOTBlYmI1ZTBjZDJhYWJlOTlkZDM4ZmQ1NDAzODExYzZiZWZiMGQ3YmMifQ%3D%3D; laravel_session=eyJpdiI6Iis0XC8xTTFmVWw4V2hUS0ZvbURDREVBPT0iLCJ2YWx1ZSI6IjRGODhVN1FFZmRJbkdXRFVHR0NCQlRPZGtsOHpYXC9tZlB6cHNFOUtST0ZVMjNJcUFNK3B1b2pLN1RMQm1qVEVmIiwibWFjIjoiZWExZmIxNTFkM2RjM2QwNWViNmZmNDI4N2JiOTJlM2M2MDcwYzcyNGNhZDY3NGE2MDNiMTM4MGRhMjgyMTk0ZiJ9'
}


for parcel_id in range(100005, 293000):
    payload=f'card=&parcelid={parcel_id}&year='
    response = requests.request("POST", url, headers=headers, data=payload)

    cleaned_response = str(response.text).replace("\\", "").strip('"')
    json_data = json.loads(cleaned_response)
    # print(cleaned_response)

    if json_data['found']:
        parcel = json_data['parcel']
        sale_date = parcel["keyinfo"][10]["value"]
        if sale_date != "-" and parcel["keyinfo"][11]["value"] != "-":

            land_info = {
                "state":"NC",
                "county":"DURHAM",
                "physical_address": str(parcel["header"]["location"]["value"]).upper().strip(),
                "property_type": " ".join(parcel["keyinfo"][5]["value"].split()).strip().upper(),
                "book": parcel["keyinfo"][8]["value"].split(" / ")[0],
                "page": parcel["keyinfo"][8]["value"].split(" / ")[1],
                "sale_date": parser.parse(sale_date),
                "sale_price": parcel["keyinfo"][11]["value"],
                "property_id": json_data["id"]
            }

            try:
                year_built = json_data["buildings"]["residential"]["display"][0]["value"]

            except KeyError:
                print(json_data["buildings"])
                break




    # break
    # expression = jmespath.compile('data.menusV3.menus[][name, groups[].[name, items[*][name,price,calories]]]')
    # #expression = jmespath.compile('length(data)')
    # data = json.loads(menu_response.text)
    # searched = expression.search(data)
