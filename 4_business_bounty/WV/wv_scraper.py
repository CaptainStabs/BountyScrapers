import requests
import csv
import os
import sys
from lxml.html import fromstring
import lxml
import usaddress
from tqdm import tqdm
import pandas as pd
import json
import random
import time
# from us_state_abbrev import us_state_abbrev

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
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document'
    }
    return headers

columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "corp_id"]

filename = "west_virginia_3.csv"

# df = pd.read_csv(filename)
# df_columns = list(df.columns)
# data_columns = ",".join(map(str, df_columns))
#
# # Get the last row from df
# last_row = df.tail(1)
# # Access the corp_id
# last_id = last_row["corp_id"].values[0]
# last_id += 1
last_id = 821342

with open(filename, "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()
# 521078                                                                       5252
    for corp_id in tqdm(range(last_id, 9999999)):
        # corp_id = 19992000
        business_info = {}
        print("\n   [*] Current ID: " + str(corp_id))
        url = f"https://apps.sos.wv.gov/business/corporations/organization.aspx?org={corp_id}"
        request_success = False
        request_tries = 0
        while not request_success or request_tries > 10:
            try:
                print("  [*] Getting results....")
                response = response = requests.request("GET", url, headers=get_user_agent(), timeout=20)
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 5...")
                time.sleep(5)
                # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                request_success = False
                request_tries += 1

            except requests.exceptions.ReadTimeout:
                print("   [!] Read timeout! Retrying in 5...")
                request_success = False
                request_tries += 1

            if request_tries > 10:
                break
        parser = fromstring(response.text)
        try:
            status_date = parser.xpath('//*[@id="tableResults"]/tr[3]/td[8]/text()')[0]
            status_reason = parser.xpath('//*[@id="tableResults"]/tr[3]/td[9]/text()')[0]

        except IndexError:
            status_date = parser.xpath('//*[@id="tableResults"]/tr[3]/td[8]/text()')
            status_reason = parser.xpath('//*[@id="tableResults"]/tr[3]/td[9]/text()')

        if not status_date and not status_reason:
            print("   [*] Exists")
            try:
                name = str(" ".join(str(parser.xpath('//*[@id="lblOrg"]/text()')[0]).upper().strip().split()))

            except IndexError:
                name = str(" ".join(str(parser.xpath('//*[@id="lblOrg"]/text()')).upper().strip().split()))
                print("      [!] Index error on name! Name: " + name)

            print("   [*] Name: " + name)

            business_type_string = str(parser.xpath('//*[@id="tableResults"]/tr[3]/td[1]/strong/text()')).upper().strip()
            print("   [*] Business type: " + business_type_string)

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
                business_info["business_type"] = "LTD"
                print("      [?] Translaetd type 2: LTD")

            if "L.T.D" in business_type_string:
                business_info["business_type"] = "LTD"
                print("      [?] Translaetd type 3: LTD")

            try:
                if not business_info["business_type"]:
                    with open("unmapped_business_type.txt", "a") as f:
                        f.write(f"{name}, {business_type_string}, {corp_id}\n")
            except Exception as e:
                print(e)



            # registered_address = ", ".join(parser.xpath('/html/body/form/div[4]/div[4]/table[4]/tr[3]/td/text()')[1:])
            # registered_address = str(" ".join(str(registered_address).upper().strip().split()))
            # print("   [*] Registered address: " + registered_address)
            fields = parser.xpath('/html/body/form/div[4]/div[4]/table[3]/tr/th/text()')

            try:
                field_index = fields.index("Principal Office Address")
                index_found = True

            except ValueError:
                print("   [!] Couldn't find principal address!")
                index_found = False

                try:
                    field_index = fields.index("Local Office Address")
                    index_found = True

                except ValueError:
                    print("   [!] Couldn't find local office address!")
                    index_found = False

            if index_found:
                # TR val is 6, but im getting 3
                field_index = field_index * 2
                # print("Fields: " + str(fields))
                # print("Field index: " + str(field_index))
                values = parser.xpath(f'/html/body/form/div[4]/div[4]/table[3]/tr[{field_index}]/td/text()')
                # /html/body/form/div[4]/div[4]/table[3]/tbody/tr[6]/td
                # print(fields[field_index])
                # print("\n")
                print("      [*]Values: " + str(values))

                # Just making this match the recycled code
                physical_address = str(", ".join(values))
                # Split and rejoin to remove and extra whitespace
                physical_address = " ".join(physical_address.upper().strip().split())
                print("   [*] Physical Address: " + str(physical_address))

            # print(parser.xpath('//*[@id="tableResults"]//tr[contains(@class, "rowNormal")]/td/text()'))

                """Physical Address parsing and cleaned_string"""
                try:
                    # address_string = str(" ".join(address_string.split()))
                    # print("      [*] Cleaned Address: " + address_string)
                    parsed_address = usaddress.tag(physical_address)
                    parse_success = True

                except usaddress.RepeatedLabelError as e:
                    print(e)
                    parse_success = False

                if parse_success:
                    try:
                        print("      [*] Parsed Address: " + str(parsed_address[0]))
                        # Split the address at the city to get the street
                        street_physical = str(physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip()
                        street_physical = street_physical.strip(",")
                        print("   [*] Street street_physical: " + str(street_physical))
                        # street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                        business_info["street_physical"] = street_physical
                        business_info["city_physical"] = parsed_address[0]["PlaceName"]
                        business_info["zip5_physical"] = parsed_address[0]["ZipCode"]
                        try:
                            business_info["state_physical"] = parsed_address[0]["StateName"]

                        except KeyError as e:
                            print(e)

                    except KeyError as e:
                        print(e)
                        try:
                            business_info["city_physical"] = parsed_address[0]["PlaceName"]
                            parse_success = True

                        except KeyError as e:
                            print(e)
                            pass
            else:
                print("   [!] This should never happen, but field_index wasn't found")

            """
            Registered Address stuff
            """
            # Slice out agent name
            registered_address = ", ".join(parser.xpath('/html/body/form/div[4]/div[4]/table[4]/tr[3]/td/text()')[1:])
            registered_address = str(" ".join(str(registered_address).upper().split()))
            print("   [*] Registered Address: " + registered_address)

            parse_success = False

            # Get physical address
            try:
                address_string = str(registered_address)
                print("      [*] Registered/Agent Address: " + address_string)
                parsed_address = usaddress.tag(address_string)
                parse_success = True

            except usaddress.RepeatedLabelError as e:
                print(e)
                parse_success = False

            if parse_success:
                try:
                    print("      [*] Parsed Address: " + str(parsed_address[0]))
                    street_registered = str(address_string.split(parsed_address[0]["PlaceName"])[0]).rstrip(",").strip()
                    street_registered = street_registered.strip(",") # Not sure why i have to do this twice
                    print("   [*] Street Registered: " + str(street_registered))
                    # street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                    business_info["street_registered"] = street_registered
                    business_info["city_registered"] = parsed_address[0]["PlaceName"]
                    business_info["zip5_registered"] = parsed_address[0]["ZipCode"]
                    try:
                        business_info["state_registered"] = parsed_address[0]["StateName"]
                    except KeyError as e:
                        print(e)
                except KeyError as e:
                    print(e)
                    try:
                        business_info["city_registered"] = parsed_address[0]["PlaceName"]
                        parse_success = True

                    except KeyError as e:
                        print(e)
                        pass

            # columns = ["filing_number", "corp_id"]
            business_info["name"] = name
            business_info["filing_number"] = corp_id
            business_info["corp_id"] = corp_id

            try:
                if business_info["business_type"]:
                    do_save = True

                # This probably wouldn't run, so I'm also putting it in the exception block
                else:
                    do_save = False
                    with open("fails_2.txt", "a") as f:
                        f.write(f"{name}, {business_type_string}, {corp_id}, business type null\n")

            except KeyError as e:
                do_save = False
                print(e)
                with open("fails_2.txt", "a") as f:
                    f.write(f"{name}, {business_type_string}, {corp_id}, key error\n")

            if do_save:
                print(json.dumps(business_info, indent=4))
                writer.writerow(business_info)






        else:
            print("   [*] Not Active: " + str(status_reason))
