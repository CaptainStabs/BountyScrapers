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
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': user_agent,
        'Content-Type': 'application/json; charset=UTF-8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    return headers

# Get Business_Id
def get_ids(business_id):
    url = "https://corp.sos.ms.gov/corp/Services/MS/CorpServices.asmx/BusinessIdSearch"

    payload = {"BusinessId":f"{business_id}"}
    payload = str(payload).replace("'", '"')
    request_tries = 0
    request_success = False
    while not request_success or request_tries > 10:
        try:
            response = requests.request("POST", url, headers=get_user_agent(), data=payload)
            request_success = True
        except requests.exceptions.ConnectionError:
            print("  [!] Connection Closed! Retrying in 5...")
            time.sleep(5)
            response = requests.request("POST", url, headers=get_user_agent(), data=payload)
            request_success = False
            request_tries += 1

        except requests.exceptions.ReadTimeout:
            print("   [!] Read timeout! Retrying in 5...")
            request_success = False
            request_tries += 1


    response_json = json.loads(response.text)
    # print(response_json)
    # print(json.dumps(response_json, indent=4))
    d_json = json.loads(response_json["d"])
    # print(d_json["Table"][0]["FilingId"])
    try:
        filing_id = d_json["Table"][0]["FilingId"]

    except TypeError:
        print("TypeError: " + str(d_json))
        filing_id = "Failed"
    return filing_id

# Get the info page
def get_info(filing_id, writer):
    if filing_id != "Failed":
        business_info = {}
        url = f"https://corp.sos.ms.gov/corp/portal/c/page/corpbusinessidsearch/~/ViewXSLTFileByName.aspx?providerName=MSBSD_CorporationBusinessDetails&FilingId={filing_id}"

        request_tries = 0
        request_success = False
        while not request_success or request_tries > 10:
            print(f"      [*] Request Tries: {request_tries}")
            try:
                proxy = "140.227.69.170"
                response = requests.request("GET", url, headers=get_user_agent())
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 5...")
                time.sleep(5)
                response = requests.request("GET", url, headers=get_user_agent())
                request_success = False
                request_tries += 1

            except requests.exceptions.ReadTimeout:
                print("   [!] Read timeout! Retrying in 5...")
                request_success = False
                request_tries += 1

            if request_tries > 10:
                break

        if request_tries > 10:
            sys.exit()

        try:
            parser = fromstring(response.text)
            parse_success = True

        except lxml.etree.ParserError as e:
            print("   [!!!] ParseError: " + str(e))
            parse_success = False

        if parse_success:
            business_status = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[3]/td[2]/text()')[0]).upper().replace("  ", " ").strip()
            if business_status == "GOOD STANDING":
                print("   [*] Status: Good Standing")
                name = str(parser.xpath('//*[@id="printDiv2"]/div[2]/table/tr[2]/td[1]/text()')[0]).upper().replace("  ", " ").strip()
                print("   [*] Name: " + name)
                business_type_string = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[1]/td[2]/text()')[0]).upper().replace("  ", " ").strip()
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
                    business_info["business_type"] = "LTD"
                    print("      [?] Translaetd type 2: LTD")

                if "L.T.D" in business_type_string:
                    business_info["business_type"] = "LTD"
                    print("      [?] Translaetd type 3: LTD")

                filing_number = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[2]/td[2]/text()')[0]).strip()
                address_string = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[6]/td[2]/text()')).upper().replace("  ", " ").strip().replace("\\XA0\\R\\N", "").replace("\\XA0", "")
                # if address_string != "[]":
                #     is_address = True
                #     address_list = address_string.strip("['']").split(",")
                #     state_zip = address_list[-1]
                #     print(address_list)
                #     print(state_zip)
                #     temp = re.compile("([a-zA-Z]+)([0-9]+)")
                #     res = temp.match(state_zip).groups()
                #     print(res)
                # else:
                #     is_address = False

                try:
                    street_address = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[6]/td[2]/text()[1]')[0]).upper().replace("  ", " ").strip()
                except IndexError:
                    street_address = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[6]/td[2]/text()[1]')).upper().replace("  ", " ").strip()
                city_state_zip = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[6]/td[2]/text()[2]')).upper().replace("  ", " ").strip().replace("\\XA0\\R\\N", "").replace("\\XA0", "").strip("[]").join(",")


                if address_string != "NO PRINCIPAL OFFICE ADDRESS FOUND":
                    business_info["street_physical"] = street_address.strip("[]")
                    # try:
                    #     print("   [*] Address " + address_string)
                    #     parsed_address = usaddress.tag(city_state_zip)
                    #     parse_success = True
                    #
                    # except usaddress.RepeatedLabelError as e:
                    #     print(e)
                    #     parse_success = False
                    #
                    # if parse_success:
                    #     # street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                    #     street_registered = city_state_zip
                    #     print(parsed_address)
                    #     business_info["street_physical"] = street_registered
                    #
                    #     try:
                    #         business_info["city_physical"] = parsed_address[0]["PlaceName"]
                    #         business_info["zip5_physical"] = parsed_address[0]["ZipCode"]
                    #         parse_success = True
                    #
                    #     except KeyError:
                    #         pass



                business_info["name"] = name
                business_info["filing_number"] = filing_number
                business_info["corp_id"] = business_id

                try:
                    incorporation_state = str(parser.xpath('//*[@id="printDiv2"]/table[1]/tr[5]/td[2]/text()')[0]).upper().replace("  ", " ").strip()
                    business_info["state_registered"] = incorporation_state
                    success = True

                except KeyError:
                    print(f"   [!!!] KeyError! State: '{incorporation_state}' is not in dictionary!")
                    success = False
                    pass

                if success:
                    writer.writerow(business_info)
            else:
                print("   [*] Status: " + business_status)
    else:
        print("   [!] Bad ID, skipping!")



filename = "mississippi.csv"
df = pd.read_csv(filename)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

# Get the last row from df
last_row = df.tail(1)
# Access the corp_id
last_id = last_row["corp_id"].values[0]
last_id += 1
# last_id =  1142457

columns = ["name", "business_type", "state_registered","street_physical","city_physical","zip5_physical", "filing_number", "corp_id"]
with open(filename, "a", encoding="utf-8", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    # business_id = 1073778                1975860
    for business_id in tqdm(range(last_id, 1975860)):
        print("\n   [*] Current id: " + str(business_id))
        get_info(get_ids(business_id), writer)
