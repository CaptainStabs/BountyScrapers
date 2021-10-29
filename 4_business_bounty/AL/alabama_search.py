import requests
from bs4 import BeautifulSoup
import usaddress
import csv
import os
import time
from tqdm import tqdm
import random

columns = ["name", "business_types", "state_registered","street_registered","city_registered","zip5_registered"]
user_agents = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
]
stats = True
def function_timer(stats):
    if stats != False:
        return time.perf_counter()


# this function simply calculates and prints the difference between the end and start times
def time_dif(stats, string, start, end):
    if stats != False:
        print(f"{string}: {end - start} seconds")


with open("alabama.csv", "a") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat("alabama.csv").st_size == 0:
        writer.writeheader()
    for corp in tqdm(range(7630, 945999)):
        business_info = {}
        corp_padded = str(corp).zfill(6)

    # print(str(corp).zfill(6))


        try:
            request_start_time = function_timer(stats)
            url = f"https://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp={corp_padded}&page=name&file=&type=ALL&status=ALL&place=ALL&city="
            print("  [*] Current business: " + str(corp_padded))
            request_end_time = function_timer(stats)
            time_dif(stats, "   [***] Request time", request_start_time, request_end_time)
            try:
                user_agent = random.choice(user_agents)
                headers = {'User-Agent': user_agent}
                response = requests.get(url, headers=headers)
            except TimeoutError:
                time.sleep(1)
                print("      [!] Timed out")
                try:
                    user_agent = random.choice(user_agents)
                    headers = {'User-Agent': user_agent}
                    response = requests.get(url, headers=headers)
                except TimeoutError:
                    time.sleep(1)
                    print("      [!] Timed out again")

                    try:
                        user_agent = random.choice(user_agents)
                        headers = {'User-Agent': user_agent}
                        response = requests.get(url, headers=headers)
                    except TimeoutError:
                        print("      [!] Timed out third time, giving up.")
                        import sys
                        sys.exit()


            except requests.exceptions.ConnectionError:
                print("      [!] ConnectionError! ")
                time.sleep(4)

                try:
                    user_agent = random.choice(user_agents)
                    headers = {'User-Agent': user_agent}
                    response = requests.get(url, headers=headers)
                except requests.exceptions.ConnectionError:
                    sys.exit()





            # print(response.status_code)
            parse_start = function_timer(stats)
            html_page = response.text
            soup = BeautifulSoup(html_page, "html.parser")
            name = soup.find("thead").find("tr").find("td").get_text()
            name = name.upper()
            state = "AL"
            print("      Name: " + str(name))
            business_info["name"] = name
            business_info["state_registered"] = state
            rows = soup.find("table").find_all("tr")
            parse_end = function_timer(stats)
            time_dif(stats, "   [***] Parse time", parse_start, parse_end)
            i = 0

            for row in rows:
                # do_save = False

                rows_data = row.find_all("td", class_="aiSosDetailValue")
                row_data_start = function_timer(stats)
                for row_data in rows_data:
                    finished = False
                    # print(row_data)
                    # if row_data.has_attr("aiSosDetailValue"):
                    # print(i)

                    if i == 1:
                        business_parse_start = function_timer(stats)
                        business_type_string = str(row_data.get_text()).upper()
                        print("      [*] Bussiness type: " + business_type_string)
                        if "COOPERATIVE" in business_type_string:
                            business_info["business_types"] = "COOP"
                            print("      [?] Translated type 1: COOP")

                        if "COOP " in business_type_string:
                            business_info["business_types"] = "COOP"
                            print("      [?] Translated type 2: COOP")

                        if "CORP " in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type 1: CORPORATION")

                        if "CORPORATION" in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type 2: CORPORATION")

                        if "DBA" in business_type_string:
                            business_info["business_types"] = "DBA"
                            print("      [?] Translated type: DBA")

                        if "LIMITED LIABILITY COMPANY" in business_type_string:
                            business_info["business_types"] = "LLC"
                            print("      [?] Translated type 1: LLC")

                        if "LLC" in business_type_string:
                            business_info["business_types"] = "LLC"
                            print("      [?] Translated type 2: LLC")

                        if "NON-PROFIT" in business_type_string:
                            business_info["business_types"] = "NONPROFIT"
                            print("      [?] Translated type 1: NON-PROFIT")

                        if "NONPROFIT" in business_type_string:
                            business_info["business_types"] = "NONPROFIT"
                            print("      [?] Translated type 2: NONPROFIT")

                        if "PARTNERSHIP" in business_type_string:
                            business_info["business_types"] = "PARTNERSHIP"
                            print("      [?] Translated type: PARTNERSHIP")

                        if "SOLE PROPRIETORSHIP" in business_type_string:
                            business_info["business_types"] = "SOLE PROPRIETORSHIP"
                            print("      [?] Translated type: SOLE PROPRIETORSHIP")

                        if "TRUST" in business_type_string:
                            business_info["business_types"] = "TRUST"
                            print("      [?] Translated type: TRUST")

                        if "INC " in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type 1: INC"))

                        if "INC" in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type 2: INC")

                        if "INCORPORATED" in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type 3: INC")

                        if "LTD" in business_type_string:
                            business_info["business_types"] = "LTD"
                            print("      [?] Translated type 1: LTD")

                        if "L.T.D" in business_type_string:
                            business_info["business_types"] = "LTD"
                            print("      [?] Translated type 1: LTD")
                        business_parse_end = function_timer(stats)
                        time_dif(stats, "   [***] Business type parsing", business_parse_start, business_parse_end)


                    if i == 2:
                        address_string = str(row_data.get_text()).upper()
                        try:
                            parsed_address = usaddress.tag(address_string)
                            print("      [?] Adderss string: " + address_string)
                            parse_success = True

                        except usaddress.RepeatedLabelError as e:
                            print(e)
                            print("       [?] Address string failed: " + address_string)
                            parse_success = False
                            pass

                        if parse_success:
                            try:
                                print("      [*] Parsed Address: " + str(parsed_address[0]))
                                street_registered = f'{parsed_address[0]["AddressNumber"]} {parsed_address[0]["StreetName"]} {parsed_address[0]["StreetNamePostType"]}'
                                business_info["street_registered"] = street_registered
                                business_info["city_registered"] = parsed_address[0]["PlaceName"]
                                business_info["zip5_registered"] = parsed_address[0]["ZipCode"]
                                parse_success = True

                            except KeyError as e:
                                print(e)
                                try:
                                    business_info["city_registered"] = parsed_address[0]["PlaceName"]
                                    parse_success = True

                                except KeyError as e:
                                    print(e)
                                    parse_success = False

                    if i == 4:
                        if str(row_data.get_text()).upper() != "EXISTS":
                            print("      [*] Not Exists: " + str(row_data.get_text()).upper())
                            do_save = False
                        else:
                            print("      [*] Exists: " + str(row_data.get_text()).upper())
                            do_save = True
                    if i <= 4:
                        # print("increment i ")
                        i += 1
                    else:
                        if do_save:
                            print("      [*] Saving")
                            writer.writerow(business_info)
                            do_save = False
                            finished = True
                            break
                            break
                        else:
                            # print("       [*] Not saving")
                            finished = True
                            break
                            break


            if finished:
                row_data_end = function_timer(stats)
                time_dif(stats, "   [***] Row_data loop time", row_data_start, row_data_end)
                break




            # break

        except AttributeError:
            pass
