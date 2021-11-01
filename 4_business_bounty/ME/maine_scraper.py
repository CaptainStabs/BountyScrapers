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
from us_state_abbrev import us_state_abbrev

def get_user_agent():
    user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    ]

    user_agent = random.choice(user_agents)
    headers = {
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="91"',
        'sec-ch-ua-mobile': '?0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchnge;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document'
    }
    return headers


columns = ["name", "business_type", "state_registered", "filing_number", "corp_id"]

filename = "maine.csv"

df = pd.read_csv(filename)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

# Get the last row from df
last_row = df.tail(1)
# Access the corp_id
last_id = last_row["corp_id"].values[0]
last_id += 1

with open(filename, "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for corp_id in tqdm(range(last_id, 19992588)):
        print("   [*] Current ID: " + str(corp_id))
        # corp_id = 19992000
        business_info = {}
        url = f"https://icrs.informe.org/nei-sos-icrs/ICRS?CorpSumm={corp_id}+D"

        response = requests.request("GET", url, headers=get_user_agent())

        parser = fromstring(response.text)
        with open("t.html", "w") as output:
            output.write(response.text)

        print(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[5]/td[4]/text()'))
        try:
            business_status = str(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[5]/td[4]/text()')[0]).upper().strip().replace("  ", " ")
            business_found = True

        except IndexError:
            print(str(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[7]/td/text()')))
            business_found = False

        if business_found:
            if business_status == "GOOD STANDING":
                print("   [*] Good Standing: " + business_status)
                do_save = True
            elif business_status == "DISSOLVED":
                print("   [*] Dissolved: " + business_status)
                do_save = False
            else:
                do_save = False
                
            if do_save:
                name = str(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[5]/td[1]/text()')[0]).upper().strip().replace("  ", " ")
                business_type_string = str(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[5]/td[3]/text()')[0]).upper().strip().replace("  ", " ")
                print("   [*] Name: " + name)
                print("   [*] Business Type: " + business_type_string)

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


                # ["name", "business_type", "state_registered","state_physical", "street_physical","city_physical","zip5_physical", "filing_number", "naics_2017", "corp_id"]
                if business_info["business_type"]:
                    business_info["name"] = name
                                                    # /html/body/center/table/tr[3]/td/table/tr[5]/td[1]/text()
                    website_state = str(parser.xpath('/html/body/center/table/tr[3]/td/table/td[3]/text()')[0]).upper().strip().replace("  ", " ")

                    try:
                        state = us_state_abbrev[website_state]
                        business_info["state_registered"] = state
                        success = True
                    except KeyError:
                        print(f"   [!!!] Key error! State: '{website_state}' is not in dictionary!")
                        success = False
                        pass

                    if success:
                        business_info["filing_number"] = str(parser.xpath('/html/body/center/table/tr[3]/td/table/tr[5]/td[2]/text()')[0])
                        business_info["corp_id"] = corp_id

                        writer.writerow(business_info)
