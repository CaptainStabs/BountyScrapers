import requests
import csv
import os
import sys
from lxml.html import fromstring
from tqdm import tqdm
import pandas as pd
import usaddress
import time
import json


payload = {}
headers = {
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}
columns = [
    "name",
    "business_type",
    "state_registered",
    "street_registered",
    "city_registered",
    "zip5_registered",
    "state_physical",
    "street_physical",
    "city_physical",
    "zip5_physical",
    "filing_number",
    "corp_id",
]

filename = "arkansas.csv"

# df = pd.read_csv(filename)
# df_columns = list(df.columns)
# data_columns = ",".join(map(str, df_columns))
#
# # Get the last row from df
# last_row = df.tail(1)
# # Access the corp_id
# last_id = last_row["corp_id"].values[0]

with open(filename, "a", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for detail_id in tqdm(range(377, 607920)):
        # detail_id = 340105
        # Convert the int to a left-padded str compatible with website
        detail_padded = str(detail_id).zfill(6)
        # Put detail_id into url
        url = f"https://www.sos.arkansas.gov/corps/search_corps.php?DETAIL={detail_padded}"
        print("   [*] Corp ID: " + str(detail_id))

        request_tries = 0
        request_success = False
        while not request_success or request_tries > 10:
            try:
                r = requests.request("GET", url, headers=headers, data=payload)
                request_success = True
            except requests.exceptions.ConnectionError:
                print("  [!] Connection Closed! Retrying in 5...")
                time.sleep(5)
                r = requests.request("GET", url, headers=headers, data=payload)
                request_success = False
                request_tries += 1

        if request_tries > 10:
            sys.exit()

        doc = fromstring(r.content)
        table = doc.xpath('.//table[@align="center"]')[0]

        print(str(table.xpath("/tr[4]/td[2]/font/text()")).strip())
        data = {
            "name": str(" ".join(str(table.xpath('tr[2]/td[2]/font/text()')[0]).upper().strip().split())),
            "ignored_name": table.xpath(".//tr[3]/td[2]/font/text()"),
            "filing_number": str(table.xpath(".//tr[4]/td[2]/font/text()")[0]).strip(),
            "business_type": str(" ".join(str(table.xpath(".//tr[5]/td[2]/font/text()")[0]).upper().strip().split())),
            "ignored_act": str(table.xpath(".//tr[6]/td[2]/font/text()")),
            "status": str(table.xpath(".//tr[7]/td[2]/font/text()")[0]).upper().strip(),
            # "principal_address": str(" ".join(str(",".join(table.xpath(".//tr[8]/td[2]/font/text()")[0])).upper().strip().split())),
            "principal_address": str(table.xpath(".//tr[8]/td[2]/font/text()")).upper().strip(),
            "reg_agent": str(table.xpath(".//tr[9]/td[2]/font/text()")[0]),
            "agent_address": str(" ".join(str(",".join(table.xpath(".//tr[10]/td[2]/font/text()"))).upper().strip().split())),
            "date_filed": table.xpath(".//tr[11]/td[2]/font/text()"),
            "officers": table.xpath(".//tr[12]/td[2]/font/text()")[0],
            "foreign_name": table.xpath(".//tr[13]/td[2]/font/text()"),
            "foreign_address": table.xpath(".//tr[14]/td[2]/font/text()"),
            "state_of_origin": str(table.xpath(".//tr[15]/td[2]/font/text()")[0]).upper().strip(),
        }
        # //*[@id="mainContent"]/table[2]/tbody/tr[2]/td[2]/font
        # //*[@id="mainContent"]/table[2]/tbody/tr[4]/td[2]/font
        # values = table.xpath('.//td[@width="375"]/font/text()')

        # data = dict(zip(fields, values))
        # print(json.dumps(data, indent=4))

        print(json.dumps(data, indent=4))

        business_status = str(data["status"]).upper().strip().replace("  ", " ")
        if business_status == "GOOD STANDING":
            print("   [*] Good Standing: " + str(data["status"]))
            do_save = True
        elif "REVOKED" in business_status:
            print("   [*] Revoked: " + str(data["status"]))
            do_save = False
        elif "DISSOLVED" in business_status:
            print("   [*] Dissolved: " + str(data["status"]))
            do_save = False
        elif "WITHDRAWN" in business_status:
            print("   [*] WITHDRAWN: " + str(data["status"]))
            do_save = False
        else:
            print("   [*] Unknown status: " + str(data["status"]))
            do_save = False

        if str(data["name"]).upper().strip().replace("  ", " ") == "N/A":
            print("   [!] Name is N/A! Not saving..:" + str(data["name"]))
            do_save = False
        # elif str(data["state_of_origin"]).upper().strip().replace("  ", " ") == "N/A":
        #     print("   [!] state_of_origin is N/A! Not saving..: " + str(data["state_of_origin"]))
        #     do_save = False

        if do_save:
            business_info = {}
            # columns = ["state_physical", "street_physical", "city_physical","zip5_physical", "filing_number", "corp_id"]
            name = data["name"]
            print("   [*] Name: " + name)
            business_info["name"] = name

            # if (
            #     len(str(data["state_of_origin"]).upper().strip().replace("  ", " "))
            #     == 2
            # ):
            #     business_info["state_registered"] = (
            #         str(data["state_of_origin"]).upper().strip().replace("  ", " ")
            #     )
            #
            # else:
            #     business_info["state_registered"] = ""

            business_info["filing_number"] = data["filing_number"]
            business_info["corp_id"] = detail_id

            # principal_address = str(table.xpath(".//tr[8]/td[2]/font/text()")[0]).upper().strip()
            principal_address = data["principal_address"]
            print(principal_address)
            if data["principal_address"] == "SAME AS REGISTERED AGENT":
                print("   [*] Principal address same as agent: " + principal_address)
                data["principal_address"] = data["agent_address"]

            else:
                temp_p_address = table.xpath(".//tr[8]/td[2]/font/text()")

                print("   [*] Temp Address var: " + str(temp_p_address))
                if type(temp_p_address) is list:
                    print("      [*] Is list")
                    if len(temp_p_address) > 1:
                        print("      [*] Is greater than 1")
                        data["principal_address"] = str(" ".join(str(",".join(table.xpath(".//tr[8]/td[2]/font/text()"))).upper().strip().split()))
                    else:
                        data["principal_address"] = str(" ".join(table.xpath(".//tr[8]/td[2]/font/text()")[0])).upper().strip()
                pass
                # principal_address = str(" ".join(table.xpath(".//tr[8]/td[2]/font/text()")[0])).upper().strip()
                # if principal_address
                # data["principal_address"] = " ".join(str(",".join(table.xpath(".//tr[8]/td[2]/font/text()")[0])).upper().strip().split()))

            # Physical address
            try:

                address_string = str(data["principal_address"]).upper().strip().replace("  ", " ")
                # address_string = str(" ".join(address_string.split()))
                # print("      [*] Cleaned Address: " + address_string)
                parsed_address = usaddress.tag(address_string)
                parse_success = True
            except usaddress.RepeatedLabelError as e:
                print(e)
                parse_success = False

            if parse_success:
                try:
                    print("      [*] Parsed Address: " + str(parsed_address[0]))
                    street_physical = str(data["principal_address"].split(parsed_address[0]["PlaceName"])[0]).rstrip(",").strip()
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

            parse_success = False

            # Get registered address
            try:
                address_string = str(data["agent_address"])
                print("      [*] Registered Address: " + address_string)
                parsed_address = usaddress.tag(address_string)
                parse_success = True

            except usaddress.RepeatedLabelError as e:
                print(e)
                parse_success = False

            if parse_success:
                try:
                    print("      [*] Parsed Address: " + str(parsed_address[0]))
                    street_registered = str(data["agent_address"].split(parsed_address[0]["PlaceName"])[0]).rstrip(",").strip()
                    print("   [*] Street Registered: " + str(street_registered))
                    # street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                    business_info["street_registered"] = street_registered
                    business_info["city_registered"] = parsed_address[0]["PlaceName"]
                    business_info["zip5_registered"] = parsed_address[0]["ZipCode"]
                    business_info["state_registered"] = parsed_address[0]["StateName"]
                except KeyError as e:
                    print(e)
                    try:
                        business_info["city_registered"] = parsed_address[0]["PlaceName"]
                        parse_success = True

                    except KeyError as e:
                        print(e)
                        pass






            business_type_string = (
                str(data["business_type"]).upper().strip().replace("  ", " ")
            )
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

            if business_info["business_type"] and business_info["state_registered"]:
                print("   [*] Business Type is not NULL, SAVING")
                writer.writerow(business_info)
            else:
                if not business_info["business_type"]:
                    print(
                        "   [*] Business Type is NULL, NOT saving: "
                        + str(business_info["business_type"])
                    )
                elif not business_info["state_registered"]:
                    print(
                        "   [*] State Registered is NULL, NOT saving: "
                        + str(data["state_of_origin"])
                        .upper()
                        .strip()
                        .replace("  ", " ")
                    )

        # print(data)
