import requests
from urllib.parse import urlparse
import csv
import json
import re
import os


headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'DNT':  '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

payload = {}


def upserve_scraper(webpage, headers, payload):
    url = "https://d2evh2mef3r450.cloudfront.net"

    print("   [*] Parsing URL...")
    parsed = urlparse(webpage) # Parse url
    web_path = parsed.path # Extract info from parse
    web_path_split = web_path.split("/")
    print(web_path_split)

    # /s/off-color-brewing-chicago/menu.json
    restaurant_name = web_path.split('/')[2].replace("-"," ").upper()
    print("   [*] Going to scrape: " + str(restaurant_name).lower())

    print("   [*] Extracting data...")
    menu_url = url + web_path + "/menu.json"
    menu_response = requests.request("GET", menu_url, headers=headers, data=payload)
    menus_json = json.loads(menu_response.text)

    print("      [*] Extracting location data....")
    location_url = f"{url}/s/{web_path_split[2]}/online_ordering.json"
    location_response = requests.request("GET", location_url, headers=headers)
    location_json = json.loads(location_response.text)

    print("         [*] Extracting location...")
    location_address = location_json["address"]
    location_city = location_address["city"].upper()
    location_state = location_address["state"]

    print("      [*] Getting Menu")
    menu = menus_json["menu"]
    menu_items = menu["items"]

    nutrition_facts = {}

    print("      [*] Creating branch name")
    branch_name = "add_" + re.sub("[^0-9a-zA-Z]+", "-", restaurant_name).lower()  # Strip out nono-alphanumeric characters
    filename = branch_name + ".csv"
    file_path = "./submited/" + filename.replace("/", "-").replace("_|_", "")

    banned_words = ["HOODIE", "GIFT CARD", "GIFTCARD", "DELIVERY FEE", "GIFT CERTIFICATE", "BANDANA", "TSHIRT"]
    columns = ["name", "restaurant_name", "identifier", "calories", "price_usd"]

    print("   [*] Opening file: " + str(file_path))
    with open(file_path, "a", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)

        # Check if the file exists, or if the file is empty
        # If it's empty, we need to add the header
        if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
            writer.writeheader()
            file_is_new = True

        else:
            print("      [*] File is not new")
            file_is_new = False

        if file_is_new:
            print("      [*] File is new")
            for item in menu_items:
                if not any(banned_word in item["name"].strip().upper() for banned_word in banned_words):
                    nutrition_facts["name"] = item["name"].strip().replace('\\"', " inch ").replace('"', " inch ").upper()
                    nutrition_facts["restaurant_name"] = restaurant_name.upper()
                    nutrition_facts["identifier"] = f"{location_city}, {location_state}"
                    nutrition_facts["price_usd"] = "{:.2f}".format(float(item["price"]))
                    # print(json.dumps(nutrition_facts, indent=4))
                    writer.writerow(nutrition_facts)
                else:
                    print("         [*] Avoiding: " + str(item["name"]))

upserve_scraper("https://app.upserve.com/s/simply-gourmet-lake-placid", headers=headers, payload=payload)
