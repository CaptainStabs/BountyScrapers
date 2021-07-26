from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse
import os
import jmespath

webpage = "https://www.toasttab.com/hearth-pizza-tavern/v3/"
url = "https://ws.toasttab.com/consumer-app-bff/v1/graphql" #  API endpoint

# use python's requests module to fetch the webpage as plain html
html_page = requests.get(webpage).text

# use BeautifulSoup4 (bs4) to parse the returned html_page using BeautifulSoup4's html parser (html.parser)
soup = BeautifulSoup(html_page, "html.parser")

# for script in soup.find_all("script")[2]:
    # try:
    #     variable_dict = json.loads(script)["window.OO_GLOBALS"]
    #     print(variable_dict)
    # except json.decoder.JSONDecodeError:
    #     pass
    # print(script)
    # variable_dict = json.loads(script)["window.OO_GLOBALS"]
    # script = script.replace("window.OO_GLOBALS =", "")

parsed = urlparse(webpage) # Parse url
web_path = parsed.path # Extract info from parse
web_path_split = web_path.split("/")
short_url = web_path_split[1]
print("   [*] Short URL: " + short_url)


print("   [*] Finding third script")
scripts = soup.find_all("script")[2]
# print("Scripts: " + str(scripts))

#  Regex? never heard of it
script = str(scripts).replace("window.OO_GLOBALS =", "").replace("<script>", "").replace("</script>", "").replace(";", "")
# print("Script: " + script)
data = json.loads(script)
restaurant_guid = data["restaurantGuid"]
print("   [*] Restaurant's guid: " + restaurant_guid)


payload = json.dumps([
    {
        "operationName": "RESTAURANT_INFO",
        "variables": {
            "restaurantGuid": f"{restaurant_guid}"
        },
        "query": "query RESTAURANT_INFO($restaurantGuid: ID!) {\n  restaurantV2(guid: $restaurantGuid) {\n    ... on Restaurant {\n      guid\n      whiteLabelName\n      location {\n        city\n        state\n }\n  }\n    ... on GeneralError {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
])
headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'apollographql-client-name': 'takeout-web',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'toast-customer-access': '',
    'content-type': 'application/json',
    'accept': '*/*',
    'apollographql-client-version': '542',
    'Toast-Restaurant-External-ID': f'{restaurant_guid}',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

response = requests.request("POST", url, headers=headers, data=payload)

parsed = json.loads(response.text)
# print(json.dumps(parsed, indent=4))
restaurant_info = parsed[0]["data"]["restaurantV2"]
city = restaurant_info["location"]["city"].upper()
state = restaurant_info["location"]["state"].upper()

restaurant_name = restaurant_info["whiteLabelName"]
identifier = f"{city}, {state}"

print("\n   [*] Restaurant Info: ")
print("      [*] Restaurant Name: " + restaurant_name)
print("      [*] Identifier: " + identifier)

menu_payload = json.dumps({
    "operationName": "MENUS",
    "variables": {
        "input": {
            "shortUrl": "okiboru",
            "restaurantGuid": f"{restaurant_guid}",
            "menuApi": "DO"
        }
    },
    "query": "query MENUS($input: MenusInput!) {\n  menusV3(input: $input) {\n    ... on MenusResponse {\n      menus {\n        id\n        name\n        groups {\n          guid\n          name\n          items {\n            description\n            guid\n            name\n            outOfStock\n            price\n            calories\n            itemGroupGuid\n            unitOfMeasure\n            usesFractionalQuantity\n            masterId\n            __typename\n          }}}}... on GeneralError {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
})
menu_response = requests.request("POST", url, headers=headers, data=menu_payload)


# print(menu_response.text)
# with open("test.json", "w") as output:
#     output.write(json.dumps(menu_parsed, indent=4))

csv_headers = ["name", "restaurant_name", "identifier", "price_usd"]
# menu_parsed = json.loads(menu_response.text)
# menus = menu_parsed["data"]["menusV3"]["menus"] # menusV3
# menu = json.dumps(menu_parsed, indent=4)
# print(menu)
expression = jmespath.compile('data.menusV3.menus[][name, groups[].[name, items[*][name,price,calories]]]')
#expression = jmespath.compile('length(data)')
data = json.loads(menu_response.text)
searched = expression.search(data)
#print(data)
print(searched)

# menu_parsed = json.loads(searched)
# print(json.dumps(menu_parsed, indent=4))
