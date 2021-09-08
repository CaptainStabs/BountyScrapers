import requests
from bs4 import BeautifulSoup
import usaddress
import csv
import os
import time
from tqdm import tqdm
from utilities.utilities import get_proxy_cycle
columns = ["name", "business_types", "state_registered","street_registered","city_registered","zip5_registered"]

def alabama_scraper(lists):
    start_id = lists[0]
    end_id = lists[1]
    file_name = lists[2]
    worker_number = lists[3]
    with open(file_name, "a") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)

        if os.stat(file_name).st_size == 0:
            writer.writeheader()
        for corp in tqdm(range(start_id, end_id)):
            business_info = {}
            corp_padded = str(corp).zfill(6)

        # print(str(corp).zfill(6))


            try:
                url = f"https://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp={corp_padded}&page=name&file=&type=ALL&status=ALL&place=ALL&city="
                print("  [*] Current business: " + str(corp_padded) + " Scraper: " + str(worker_number))
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
                # print("      Name: " + str(name))
                business_info["name"] = name
                business_info["state_registered"] = state
                rows = soup.find("table").find_all("tr")
                i = 0
                for row in rows:
                    # do_save = False

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

                        if i == 2:
                            address_string = str(row_data.get_text()).upper()
                            try:
                                parsed_address = usaddress.tag(address_string)
                                # print("      [?] Adderss string: " + address_string)
                                parse_success = True

                            except usaddress.RepeatedLabelError as e:
                                print(e)
                                # print("       [?] Address string failed: " + address_string)
                                parse_success = False
                                pass

                            if parse_success:
                                try:
                                    # print("      [*] Parsed Address: " + str(parsed_address[0]))
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
                                do_save = False
                                break
                                break
                            else:
                                # print("       [*] Not saving")
                                break
                                break




                # break

            except AttributeError:
                pass

def alabama_scraper_proxy(lists):
    import requests
    from bs4 import BeautifulSoup
    import usaddress
    import csv
    import os
    import time
    from tqdm import tqdm
    from utilities.utilities import get_proxy_cycle, get_open_proxy_cycle
    columns = ["name", "business_types", "state_registered","street_registered","city_registered","zip5_registered"]

    def alabama_scraper(lists):
        # proxy_cycle = get_proxy_cycle()
        proxy_cycle = get_open_proxy_cycle()
        start_id = lists[0]
        end_id = lists[1]
        file_name = lists[2]
        worker_number = lists[3]
        with open(file_name, "a") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=columns)

            if os.stat(file_name).st_size == 0:
                writer.writeheader()
            for corp in tqdm(range(start_id, end_id)):
                business_info = {}
                corp_padded = str(corp).zfill(6)

            # print(str(corp).zfill(6))


                try:
                    proxy = next(proxy_cycle)
                    url = f"https://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp={corp_padded}&page=name&file=&type=ALL&status=ALL&place=ALL&city="
                    print("  [*] Current business: " + str(corp_padded) + " Scraper: " + str(worker_number))
                    try:
                        response = requests.get(url, proxies={"http": proxy, "https": proxy})
                    except TimeoutError:
                        time.sleep(0.9)
                        print("      [!] Timed out")
                        try:
                            response = requests.get(url, proxies={"http": next(proxy_cycle), "https": next(proxy_cycle)})
                        except TimeoutError:
                            time.sleep(0.5)
                            print("      [!] Timed out again")

                            try:
                                response = requests.get(url, proxies={"http": next(proxy_cycle), "https": next(proxy_cycle)})
                            except TimeoutError:
                                print("      [!] Timed out third time, giving up.")
                                import sys
                                sys.exit()


                    except requests.exceptions.ConnectionError:
                        print("      [!] ConnectionError! 1")
                        print("         [*] Proxy: " + str(proxy))
                        time.sleep(4)

                        try:
                            proxy = next(proxy_cycle)
                            print(proxy)
                            response = requests.get(url, proxies={"http": proxy, "https": proxy})

                        except requests.exceptions.ConnectionError as e:
                            print(e)
                            time.sleep(1)
                            print("      [!] ConnectionError! 2")
                            print("         [*] Proxy: " + str(proxy))
                            try:
                                proxy = next(proxy_cycle)
                                response = requests.get(url, proxies={"http": proxy, "https": proxy})

                            except requests.exceptions.ConnectionError:
                                print("      [!] ConnectionError! 3")
                                print("         [*] Proxy: " + str(proxy))
                                time.sleep(1)
                                try:
                                    proxy = next(proxy_cycle)
                                    response = requests.get(url, proxies={"http": proxy, "https": proxy})

                                except requests.exceptions.ConnectionError:
                                    print("      [!] ConnectionError! 4")
                                    print("         [*] Proxy: " + str(proxy))
                                    time.sleep(1)
                                    try:
                                        proxy = next(proxy_cycle)
                                        response = requests.get(url, proxies={"http": proxy, "https": proxy})
                                        print("         [*] Proxy: " + str(proxy))

                                    except requests.exceptions.ConnectionError:
                                        time.sleep(1)
                                        print("      [!] ConnectionError! 5")
                                        print("         [*] Proxy: " + str(proxy))
                                        try:
                                            proxy = next(proxy_cycle)
                                            response = requests.get(url, proxies={"http": proxy, "https": proxy})

                                        except requests.exceptions.ConnectionError:
                                            time.sleep(1)
                                            print("      [!] ConnectionError! 6")
                                            print("         [*] Proxy: " + str(proxy))
                                            try:
                                                proxy = next(proxy_cycle)
                                                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                                            except requests.exceptions.ConnectionError:
                                                time.sleep(1)
                                                print("      [!] ConnectionError! Final 7")
                                                print("         [*] Proxy: " + str(proxy))
                                                import sys
                                                sys.exit()





                    # print(response.status_code)
                    html_page = response.text
                    soup = BeautifulSoup(html_page, "html.parser")
                    name = soup.find("thead").find("tr").find("td").get_text()
                    name = name.upper()
                    state = "AL"
                    # print("      Name: " + str(name))
                    business_info["name"] = name
                    business_info["state_registered"] = state
                    rows = soup.find("table").find_all("tr")
                    i = 0
                    for row in rows:
                        # do_save = False

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

                            if i == 2:
                                address_string = str(row_data.get_text()).upper()
                                try:
                                    parsed_address = usaddress.tag(address_string)
                                    # print("      [?] Adderss string: " + address_string)
                                    parse_success = True

                                except usaddress.RepeatedLabelError as e:
                                    print(e)
                                    # print("       [?] Address string failed: " + address_string)
                                    parse_success = False
                                    pass

                                if parse_success:
                                    try:
                                        # print("      [*] Parsed Address: " + str(parsed_address[0]))
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
                                    do_save = False
                                    break
                                    break
                                else:
                                    # print("       [*] Not saving")
                                    break
                                    break




                    # break

                except AttributeError:
                    pass
