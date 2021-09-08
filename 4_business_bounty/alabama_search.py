import requests
from bs4 import BeautifulSoup
import usaddress
import csv
import os
import time
from tqdm import tqdm
columns = ["name", "business_types", "state_registered","street_registered","city_registered","zip5_registered"]

with open("alabama.csv", "a") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat("alabama.csv").st_size == 0:
        writer.writeheader()
    for corp in tqdm(range(4646, 945999)):
        business_info = {}
        corp_padded = str(corp).zfill(6)

    # print(str(corp).zfill(6))


        try:
            url = f"https://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp={corp_padded}&page=name&file=&type=ALL&status=ALL&place=ALL&city="
            print("  [*] Current business: " + str(corp_padded))
            try:
                response = requests.get(url)
            except TimeoutError:
                time.sleep(4)
                print("      [!] Timed out")
                try:
                    response = requests.get(url)
                except TimeoutError:
                    time.sleep(4)
                    print("      [!] Timed out again")

                    try:
                        response = requests.get(url)
                    except TimeoutError:
                        print("      [!] Timed out third time, giving up.")
                        import sys
                        sys.exit()


            except requests.exceptions.ConnectionError:
                print("      [!] ConnectionError! ")
                time.sleep(4)

                try:
                    response = requests.get(url)
                except requests.exceptions.ConnectionError:
                    sys.exit()





            # print(response.status_code)
            html_page = response.text
            soup = BeautifulSoup(html_page, "html.parser")
            name = soup.find("thead").find("tr").find("td").get_text()
            name = name.upper()
            state = "AL"
            print("      Name: " + str(name))
            business_info["name"] = name
            business_info["state_registered"] = state
            rows = soup.find("table").find_all("tr")
            i = 0
            for row in rows:
                rows_data = row.find_all("td", class_="aiSosDetailValue")
                for row_data in rows_data:
                    # print(row_data)
                    # if row_data.has_attr("aiSosDetailValue"):
                    # print(i)
                    if i == 1:
                        business_type_string = str(row_data.get_text()).upper()
                        print("      [*] Bussiness type: " + business_type_string)
                        if "COOPERATIVE" in business_type_string:
                            business_info["business_types"] = "COOP"
                            print("      [?] Translated type: COOP")

                        if "COOP " in business_type_string:
                            business_info["business_types"] = "COOP"
                                print("      [?] Translated type: COOP")

                        if "CORP " in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type: CORPORATION")

                        if "CORPORATION" in business_type_string:
                            business_info["business_types"] = "CORPORATION"
                            print("      [?] Translated type: CORPORATION")

                        if "DBA" in business_type_string:
                            business_info["business_types"] = "DBA"
                            print("      [?] Translated type: DBA")

                        if "LIMITED LIABILITY COMPANY" or "LLC" in business_type_string:
                            business_info["business_types"] = "LLC"
                            print("      [?] Translated type: LLC")

                        if "NON-PROFIT" or "NONPROFIT" in business_type_string:
                            business_info["business_types"] = "NONPROFIT"
                            print("      [?] Translated type: NONPROFIT")

                        if "PARTNERSHIP" in business_type_string:
                            business_info["business_types"] = "PARTNERSHIP"
                            print("      [?] Translated type: PARTNERSHIP")

                        if "SOLE PROPRIETORSHIP" in business_type_string:
                            business_info["business_types"] = "SOLE PROPRIETORSHIP"
                            print("      [?] Translated type: SOLE PROPRIETORSHIP")

                        if "TRUST" in business_type_string:
                            business_info["business_types"] = "TRUST"
                            print("      [?] Translated type: TRUST")

                    if i == 2:
                        address_string = str(row_data.get_text()).upper()
                        try:
                            parsed_address = usaddress.tag(address_string)
                            parse_success = True

                        except usaddress.RepeatedLabelError as e:
                            print(e)
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
                        i += 1
                    else:
                        if do_save:
                            print("      [*] Saving")
                            writer.writerow(business_info)
                        break



            # break

        except AttributeError:
            pass
