import requests
import requests
from lxml.html import fromstring
from tqdm import tqdm
import csv
import os
import random
import pandas as pd
import usaddress

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
        'sec-ch-ua-mobile': '?0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        # 'Cookie': 'ASP.NET_SessionId=lfc1hkbd34bfrtpjkhktmgjq'
    }

payload={}


columns = ["name", "business_type", "state_registered","state_physical", "street_physical","city_physical","zip5_physical", "filing_number", "naics_2017", "corp_id"]
file_name = "rhode_island.csv"

df = pd.read_csv(file_name)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

# Get the last row from df
last_row = df.tail(1)
# Access the corp_id
last_id = last_row["corp_id"].values[0]
last_id += 1

# last_id = 1

with open(file_name, "a", encoding="utf8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(file_name).st_size == 0:
        writer.writeheader()

    for id_number in tqdm(range(last_id, 165688)):
        business_info = {}
        # print("\n" + str(id_number))
        padded_id = str(id_number).zfill(9)
        url = f"https://business.sos.ri.gov/CorpWeb/CorpSearch/CorpSummary.aspx?FEIN={padded_id}&SEARCH_TYPE=1"
        response = requests.request("GET", url, headers=get_user_agent())

        parser = fromstring(response.text)

        inactive_date_label = str(parser.xpath('//*[@id="MainContent_lblInactiveDateLabel"]/text()')).upper().strip().replace("  ", " ")

        if "DISSOLUTION" in inactive_date_label:
            print("   [*] Dissolution: " + inactive_date_label)
            do_save = False
        elif "REVOCATION" in inactive_date_label:
            print("   [*] Revoked: " + inactive_date_label)
            do_save = False

        elif "WITHDRAWAL" in inactive_date_label:
            print("   [*] Withdrawn: " + inactive_date_label)
            do_save = False

        else:
            print("  [*] Still Exists: " + inactive_date_label)
            do_save = True


        if do_save:
            name = str(parser.xpath('//*[@id="MainContent_lblEntityName"]/text()'))[2:-2].upper().strip().replace("  ", " ")
            business_type_string = str(parser.xpath('//*[@id="MainContent_lblEntityType"]/text()'))[2:-2].upper().strip().replace("  ", " ")
            print("\n   [*] Name: " + name)
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


            if business_type_string:
                business_info["name"] = name
                business_info["state_registered"] = "RI"
                business_info["state_physical"] = str(parser.xpath('//*[@id="MainContent_lblPrincipleState"]/text()'))[2:-2].upper().strip().replace("  ", " ")
                business_info["street_physical"] = str(parser.xpath('//*[@id="MainContent_lblPrincipleStreet"]/text()'))[2:-2].upper().strip().replace("  ", " ")
                business_info["city_physical"] = str(parser.xpath('//*[@id="MainContent_lblOfficeCity"]/text()'))[2:-2].upper().strip().replace("  ", " ")
                business_info["zip5_physical"] = str(parser.xpath('//*[@id="MainContent_lblOfficeZip"]/text()'))[2:-2].strip().replace("  ", " ")
                business_info["filing_number"] = padded_id
                business_info["naics_2017"] = str(parser.xpath('//*[@id="MainContent_txtNIACS"]/@value'))[2:-2].split(" ")[0]
                business_info["corp_id"] = padded_id
                print("   [*] NAICS_2017: " + str(parser.xpath('//*[@id="MainContent_txtNIACS"]/@value'))[2:-2].split(" ")[0])
                writer.writerow(business_info)





        # print(parser.xpath('//*[@id="MainContent_lblPrincipleStreet"]/text()'))
        # print(parser.xpath('//*[@id="MainContent_lblInactiveDateLabel"]/text()'))
