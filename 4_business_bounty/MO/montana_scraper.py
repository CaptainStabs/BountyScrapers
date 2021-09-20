import requests
import csv
import os
import sys
import usaddress
from tqdm import tqdm
import pandas as pd
import json
import random
import re
import time

# Get random user agent
def get_user_agent():
    user_agents = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]

    user_agent = random.choice(user_agents)
    headers = {
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'authorization': 'undefined',
        'DNT': '1',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': user_agent,
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        # 'Cookie': 'ASP.NET_SessionId=jefspg33q1c5aecdh5bh0tnj'
    }

    return headers


file_name = "montana.csv"
url = "https://biz.sosmt.gov/api/Records/businesssearch"
columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "state_physical", "city_physical", "zip5_physical", "filing_number", "corp_id"]
with open(file_name, "a", encoding="utf8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(file_name).st_size == 0:
        writer.writeheader()

    for search_value in tqdm(range(2030, 999999)):
        business_info = {}
        business_info["corp_id"] = str(search_value).zfill(6) # I don't want "A"/letter in it as it's used to start loops
        padded_search_value = "A" + str(search_value).zfill(6)
        print("\n\n   [*] Current business ID: " + padded_search_value)
        payload = json.dumps({
            "SEARCH_VALUE": f"{padded_search_value}",
            "STARTS_WITH_YN": True,
            "FILING_TYPE_ID": "0",
            "FILING_SUBTYPE_ID": "0",
            "STATUS_ID": "0",
            "STATE": "",
            "COUNTY": "",
            "CRA_SEARCH_YN": False,
            "FILING_DATE": {
                "start": None,
                "end": None
            },
            "EXPIRATION_DATE": {
                "start": None,
                "end": None
            }
        })


        request_success = False
        request_tries = 0
        while not request_success or request_tries > 10:
            try:
                response = requests.request("POST", url, headers=get_user_agent(), data=payload)
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 5...")
                time.sleep(5)
                # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                request_success = False
                request_tries += 1

        parsed_json = json.loads(response.text)

        # print(json.dumps(parsed_json, indent=4))

        if bool(parsed_json["rows"]):
            # Get the id from the unknown key after `rows`
            url_id = next(iter(parsed_json["rows"]))
            print("   [*] url_id: " + str(url_id))

            if str(parsed_json["rows"][url_id]["STATUS"]).upper().strip().replace("  ", " ") == "ACTIVE":
                business_info["name"] = str(parsed_json["rows"][url_id]["TITLE"][0]).upper().strip().replace("  ", " ").replace(f"({padded_search_value})", "")
                print("   [*] Name: " + business_info["name"])

                url = f"https://biz.sosmt.gov/api/FilingDetail/business/{url_id}/false"

                while not request_success or request_tries > 10:
                    try:
                        response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                        request_success = True
                    except requests.exceptions.ConnectionError:
                        print("  [!] Connection Closed! Retrying in 5...")
                        time.sleep(5)
                        # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                        request_success = False
                        request_tries += 1

                business_data = json.loads(response.text)
                business_data = business_data["DRAWER_DETAIL_LIST"]


                for i in range(len(business_data)):
                    # I could just assume that the list's order will always be the same, but I don't trust it enough
                    business_dict = business_data[i]
                    if business_dict["LABEL"] == "Filing Number":
                        business_info["filing_number"] = filing_dict["VALUE"]

                    if business_dict["LABEL"] == "Entity SubType":
                        business_type_string = str(business_dict["VALUE"]).upper().strip()
                        print("   [*] Business Type String: " + business_type_string)
                        if "COOPERATIVE" in business_type_string:
                            business_info["business_type"] = "COOP"
                            print("      [?] Translated type 1: COOP")

                        if "COOP " in business_type_string:
                            business_info["business_type"] = "COOP"
                            print("      [?] Translated type 2: COOP")
                        if "CORP" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 1: CORPORATION")

                        if "CORP " in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 2: CORPORATION")

                        if "CORPORATION" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 3: CORPORATION")

                        if "DBA" in business_type_string:
                            business_info["business_type"] = "DBA"
                            print("      [?] Translated type: DBA")

                        if "LIMITED LIABILITY COMPANY" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 1: LLC")

                        if "LLC" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 2: LLC")

                        if "L.L.C." in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 3: LLC")

                        if "L.L.C" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 4: LLC")

                        if "NON-PROFIT" in business_type_string:
                            business_info["business_type"] = "NONPROFIT"
                            print("      [?] Translated type 1: NON-PROFIT")

                        if "NONPROFIT" in business_type_string:
                            business_info["business_type"] = "NONPROFIT"
                            print("      [?] Translated type 2: NONPROFIT")

                        if "PARTNERSHIP" in business_type_string:
                            business_info["business_type"] = "PARTNERSHIP"
                            print("      [?] Translated type: PARTNERSHIP")

                        if "SOLE PROPRIETORSHIP" in business_type_string:
                            business_info["business_type"] = "SOLE PROPRIETORSHIP"
                            print("      [?] Translated type: SOLE PROPRIETORSHIP")

                        if "TRUST" in business_type_string:
                            business_info["business_type"] = "TRUST"
                            print("      [?] Translated type: TRUST")

                        if "INC " in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 1: INC")

                        if "INC" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 2: INC")

                        if "INCORPORATED" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 3: INC")

                        # if "LIMITED" in business_type_string:
                        #     business_info["business_type"] = "LTD"
                        #     print("      [?] Translaetd type1: LTD")

                        if "LTD" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translaetd type 2: LLC")

                        if "L.T.D" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translaetd type 3: LLC")

                        if "INDIVIDUAL" in business_type_string:
                            business_info["business_type"] = "SOLE PROPRIETORSHIP"
                            print("      [?] Translated Type: SOLE PROPRIETORSHIP")

                    if business_dict["LABEL"] == "Principal Address":
                        if str(business_dict["VALUE"]).upper().strip() != "N/A":
                            print("   [*] Principal Address Not N/A: " + str(business_dict["VALUE"]))

                            address_string = str(business_dict["VALUE"]).upper().strip().replace(",,", ",")
                            address_string = str(" ".join(address_string.split()))

                            try:
                                parsed_address = usaddress.tag(address_string)
                                print(parsed_address)
                                parse_success = True

                            except usaddress.RepeatedLabelError as e:
                                print(e)
                                parse_success = False


                            if parse_success:
                                try:
                                    street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                                    business_info["street_physical"] = street_registered
                                    business_info["city_physical"] = parsed_address[0]["PlaceName"]
                                    business_info["zip5_physical"] = parsed_address[0]["ZipCode"]

                                except KeyError as e:
                                    print("   [!] KeyError, Trying again: ")
                                    print(e)

                                    try:
                                        business_info["city_physical"] = parsed_address[0]["PlaceName"]
                                        business_info["zip5_physical"] = parsed_address[0]["ZipCode"]
                                    except KeyError as e:
                                        print("      [!] Failed a second time! Giving up...")

                    if business_dict["LABEL"] == "Mailing Address":
                        if str(business_dict["VALUE"]).upper().strip() != "N/A":
                            print("   [*] Mailing Address is not N/A: " + str(business_dict["VALUE"]).upper().strip())
                            address_string = str(business_dict["VALUE"]).upper().strip().replace(",,", ",")
                            address_string = str(" ".join(address_string.split()))

                            try:
                                parsed_address = usaddress.tag(address_string)
                                print(parsed_address)
                                parse_success = True

                            except usaddress.RepeatedLabelError as e:
                                print(e)
                                parse_success = False


                            if parse_success:
                                try:
                                    street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                                    business_info["street_registered"] = street_registered
                                    business_info["city_registered"] = parsed_address[0]["PlaceName"]
                                    business_info["zip5_registered"] = parsed_address[0]["ZipCode"]

                                except KeyError as e:
                                    print("   [!] KeyError, Trying again: ")
                                    print(e)

                                    try:
                                        business_info["city_registered"] = parsed_address[0]["PlaceName"]
                                        business_info["zip5_registered"] = parsed_address[0]["ZipCode"]
                                    except KeyError as e:
                                        print("      [!] Failed a second time! Giving up...")
                        else:
                            print("   [*] Mailing Address IS N/A: " + str(business_dict["VALUE"]).upper().strip())

                writer.writerow(business_info)




            else:
                print("   [*] Not Active: " + str(parsed_json["rows"][url_id]["STATUS"]).upper().strip().replace("  ", " ") + "\n")




            # print(json.dumps(business_data, indent=4))
