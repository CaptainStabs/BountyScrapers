from multiprocessing import Pool
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
import logging
import traceback as tb

class KeyboardInterruptError(Exception):
    pass

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

def get_last_id(filename):
    if os.path.exists(filename) and os.stat(filename).st_size > 227:
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        try:
            last_id = last_row["filing_number"].values[0]
            last_id += 1
            return last_id
        except IndexError:
            print("  [!] File likely did not have any data other than header. " + str(filename))
            last_id = 1
            return last_id
    else:
        last_id = 1
        return

def scraper(filename, start_num, end_id):
    # print("Startnum: " + str(start_num))
    # print("Endnum: " + str(end_id))
    url = "https://biz.sosmt.gov/api/Records/businesssearch"
    columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "corp_id"]

    logging.basicConfig(filename='threads.log')
    try:
        with open(filename, "a", encoding="utf8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=columns)

            if os.path.exists(filename) and os.stat(filename).st_size > 4:
                start_id = get_last_id(filename)

            else:
                start_id = start_num

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            for search_value in tqdm(range(start_id, end_id)):
                print("   [*] Current ID: " + str(search_value))
                s = requests.Session()
                s.headers.update(get_user_agent())
                business_info = {}
                business_info["corp_id"] = search_value

                request_success = False
                request_tries = 0
                url = f"https://biz.sosmt.gov/api/FilingDetail/business/{search_value}/false"

                while not request_success or request_tries > 10:
                    try:
                        print("  [*] Getting results....")
                        response = s.request("GET", url)
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



                business_data = json.loads(response.text)
                # print(business_data)
                try:
                    business_data = business_data["DRAWER_DETAIL_LIST"]
                    business_parse_success = True
                except KeyError:
                    # logging.error("AAAAAAA:\n    " + str(response.text))
                    business_parse_success = False

                if business_parse_success:
                    for i in range(len(business_data)):
                        # I could just assume that the list's order will always be the same, but I don't trust it enough
                        business_dict = business_data[i]
                        if business_dict["LABEL"] == "Status":
                            if business_dict["VALUE"] == "Active-Good Standing" or business_dict["VALUE"] == "Active":
                                print("   [*] Business active: " + str(business_dict["VALUE"]))
                                do_save = True
                                continue
                            else:
                                print("   [*] Business not active: " + str(business_dict["VALUE"]))
                                do_save = False
                                break
                        if business_dict["LABEL"] == "Filing Number":
                            business_info["filing_number"] = business_dict["VALUE"]

                        if business_dict["LABEL"] == "Entity SubType":
                            business_type_string = str(business_dict["VALUE"]).upper().strip()
                            print("   [*] Business Type String: " + business_type_string)
                            if "ASSUMED BUSINESS NAME" in business_type_string:
                                business_info["business_type"] = "DBA"
                                print("      [?] Translated type: DBA")

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

                            if "FICTITIOUS NAME" in business_type_string:
                                business_info["business_type"] = "DBA"
                                print("      [?] Translated Type: DBA")

                            if "ASSUMED BUSINESS NAME" in business_type_string:
                                business_info["business_type"] = "DBA"
                                print("      [?] Translated Type: DBA")

                            try:
                                print(business_info["business_type"])
                            except KeyError:
                                print("      [!] No business type defined, defaulting to CORPORATION")
                                business_info["business_type"] = "CORPORATION"


                        if business_dict["LABEL"] == "Principal Address":
                            if str(business_dict["VALUE"]).upper().strip() != "N/A":
                                # print("   [*] Principal Address Not N/A: " + str(business_dict["VALUE"]))

                                address_string = str(business_dict["VALUE"]).upper().strip().replace(",,", ",")
                                address_string = str(" ".join(address_string.split()))

                                try:
                                    parsed_address = usaddress.tag(address_string)
                                    # print(parsed_address)
                                    parse_success = True

                                except usaddress.RepeatedLabelError as e:
                                    print(e)
                                    parse_success = False


                                if parse_success:
                                    try:
                                        street_physical = str(address_string).split(parsed_address[0]["PlaceName"])[0]
                                        street_physical = street_physical.strip(",").strip().upper()
                                        business_info["street_physical"] = street_physical
                                    except KeyError:
                                        pass
                                    try:
                                        business_info["city_physical"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().upper().split())
                                    except KeyError:
                                        pass
                                        # print("      [!] City physical parse failure!")

                                    try:
                                        business_info["zip5_physical"] = str(parsed_address[0]["ZipCode"]).strip()

                                    except KeyError:
                                        pass

                                    try:
                                        business_info["state_physical"] = str(parsed_address[0]["StateName"]).strip().upper()
                                    except KeyError:
                                        pass

                        if business_dict["LABEL"] == "Registered Agent":
                            if str(business_dict["VALUE"]).upper().strip() != "N/A" or str(business_dict["VALUE"].upper().strip() != "NO AGENT"):
                                # print("   [*] Registered Agent is not N/A: " + str(business_dict["VALUE"]).upper().strip())
                                address_list = str(business_dict["VALUE"]).upper().strip().replace(",,", ",").split("\n")
                                # print("      [*] Registered Agent string: " + str(address_list))
                                address_string = ", ".join(address_list[3:])
                                address_string = str(" ".join(address_string.split()))
                                # print("         [*] Address string with agent stripped: " + address_string)

                                try:
                                    parsed_registered_address = usaddress.tag(address_string)
                                    # print(parsed_address)
                                    parse_success = True

                                except usaddress.RepeatedLabelError as e:
                                    logging.exception("Failed to parse address")
                                    print(e)
                                    parse_success = False


                                if parse_success:
                                    try:
                                        street_registered = str(address_string).split(parsed_registered_address[0]["PlaceName"])[0]
                                        street_registered = street_registered.strip(",").strip().upper()
                                        business_info["street_registered"] = street_registered
                                    except KeyError:
                                        pass

                                    try:
                                        business_info["city_registered"] = " ".join(str(parsed_registered_address[0]["PlaceName"]).strip(",").strip().upper().split())
                                    except KeyError:
                                        pass
                                        # print("      [!] City Registered parse failure!")

                                    try:
                                        business_info["zip5_registered"] = str(parsed_registered_address[0]["ZipCode"]).strip()

                                    except KeyError:
                                        pass

                                    try:
                                        business_info["state_registered"] = str(parsed_registered_address[0]["StateName"]).strip().upper()

                                    except KeyError:
                                        pass
                            else:
                                print("   [*] Registered Agent IS N/A: " + str(business_dict["VALUE"]).upper().strip())


                    if do_save:

                        payload = json.dumps({
                            "SEARCH_VALUE": business_info["filing_number"],
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

                        search_url = "https://biz.sosmt.gov/api/Records/businesssearch"
                        request_success = False
                        request_tries = 0
                        while not request_success or request_tries > 10:
                            try:
                                print("  [*] Getting results....")
                                response = s.request("POST", search_url, data=payload)
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

                        try:
                            parsed_json = json.loads(response.text)
                            json_parsed = True

                        except Exception as e:
                            print("Error parsing JSON response")
                            json_parsed = False

                        # print(response.text)
                        if json_parsed:
                            if bool(parsed_json["rows"]):
                                url_id = next(iter(parsed_json["rows"]))
                                # print("   [*] url_id: " + str(url_id))
                                name = str(parsed_json["rows"][url_id]["TITLE"][0]).upper().strip().replace("  ", " ").replace(f"({business_info['filing_number']})", "")
                                name = " ".join(name.split())
                                print("   [*]  Name: " + name)
                                business_info["name"] = name


                                writer.writerow(business_info)


    except KeyboardInterrupt:
        raise KeyboardInterruptError()

    except Exception as e:
        logging.exception("\n" + str(e))
        raise
        pass

if __name__ == '__main__':
    arguments = []

    # Total divided by 40
    end_id = 250000
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(40):
        if i == 0:
            start_num = 0
        else:
            # Use end_id before it is added to
            start_num = end_id - 250000
        # print("Startnum: " + str(start_num))
        arguments.append((f"./files/mt_{i}.csv", start_num, end_id))
        end_id = end_id + 250000
    # print(arguments)
    try:
        pool = Pool(processes=40)
        pool.starmap(scraper, arguments)
        pool.close()
    except KeyboardInterrupt:
        print("   [!] Caught KeyboardInterrupt! Terminating and joining pool...")
        pool.close()
        # pool.join()
    except IndexError as e:
        print(e)
        tb.print_exc()
        print("   [!] Weird pandas/numpy/multithreadding problem, passing")
        pass
    except Exception as e:
        print(e)
        logging.exception(e)
        tb.print_exc()
        pool.close()
        # pool.join()
    finally:
        print("   [*] Joining pool...")
        pool.join()
        print("   [*] Finished joining...")
