import requests
from lxml.html import fromstring
from tqdm import tqdm
from us_state_abbrev import us_state_abbrev
import csv
import os
import random
import pandas as pd




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
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document'
    }
    return headers

payload={}

columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "filing_number", "corp_id"]
file_name = "oklahoma.csv"

df = pd.read_csv("oklahoma.csv")
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

# Get the last row from df
last_row = df.tail(1)
# Access the corp_id
last_id = last_row["corp_id"].values[0]
last_id += 1

# last_id = 1900007095

with open(file_name, "a", encoding="utf8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(file_name).st_size == 0:
        writer.writeheader()

    for corp_id in tqdm(range(last_id, 1900246779)):
    # corp_id = 3512384626
        business_info = {}
        print(corp_id)
        url = f"https://www.sos.ok.gov/corp/corpInformation.aspx?id={corp_id}"
        response = requests.request("GET", url, headers=get_user_agent(), data=payload)
        parser = fromstring(response.text)

        status = parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()')


        if "EXISTENCE" in str(status[0]).strip().upper():
            print("\n   [*] Exists: " + str(status[0]).strip())

            name = str(parser.xpath('//*[@id="printDiv"]/h3/text()')[0]).strip().upper().replace("  ", " ")
            business_type_string = str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[4]/text()')[0]).strip().upper().replace("  ", " ")
            print("\n   [*] Name: " + name)
            print("\n   [*] Type: " + business_type_string)

            business_info["name"] = name
            business_info["corp_id"] = corp_id

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

            website_state = str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[5]/text()')[0]).strip().upper().replace("  ", " ")
            filing_number = str(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[1]/text()')[0]).strip().replace("  ", " ")
            print("FilingNumber: " + filing_number)
            # This is the same as the corp_id but just in case
            business_info["filing_number"] = filing_number

            try:
                state = us_state_abbrev[website_state]
                business_info["state_registered"] = state
                success = True
            except KeyError:
                print(f"   [!!!] Key error! State: '{website_state}' is not in dictionary!")
                success = False
                pass

            if business_type_string and success:
                writer.writerow(business_info)

            elif not business_type_string and success:
                with open("fails.csv", "a", encoding="utf-8") as fail_output:
                    fail_writer = csv.DictWriter(fail_output, fieldnames=columns)

                    if os.stat("fails.csv").st_size == 0:
                        fail_writer.writeheader()

                    fail_writer.writerow(business_info)

            elif not success:
                with open("not_success.csv", "a", encoding="utf-8") as not_success:
                    not_success_writer = csv.DictWriter(not_success, fieldnames=columns)

                    if os.stat("not_success.csv").st_size == 0:
                        not_success_writer.writeheader()

                    not_success_writer.writerow(business_info)

            # print(parser.xpath('//*[@id="printDiv"]/dl[1]/dd[3]/text()'))

            # print(response.text)

        else:
            print("\n Not Exists: " + str(status[0]).strip().upper())
