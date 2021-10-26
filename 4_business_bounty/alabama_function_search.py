import requests
from bs4 import BeautifulSoup
import usaddress
import csv
import os
import time
from tqdm import tqdm
from utilities.utilities import get_proxy_cycle
import random

columns = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "corp_id"]

class KeyboardInterruptError(Exception):
    pass

def function_timer(stats):
    if stats != False:
        return time.perf_counter()


# this function simply calculates and prints the difference between the end and start times
def time_dif(stats, string, start, end):
    if stats != False:
        print(f"{string}: {end - start} seconds")
def get_user_agent():
    user_agents = user_agents = [
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


def alabama_scraper(lists):
    user_agents = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4389.72 Mobile Safari/537.36'
]
    try:
        start_id = lists[0]
        end_id = lists[1]
        file_name = lists[2]
        worker_number = lists[3]
        with open(file_name, "a", encoding="utf-8", newline="") as output_file:
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
                        response = requests.get(url, headers=get_user_agent())
                        print("   [*] Cookies: " + str(response.cookies))
                    except TimeoutError:
                        time.sleep(4)
                        print("      [!] Timed out")
                        try:
                            response = requests.get(url, headers=get_user_agent())
                        except TimeoutError:
                            time.sleep(4)
                            print("      [!] Timed out again")

                            try:
                                response = requests.get(url, headers=get_user_agent())
                            except TimeoutError:
                                print("      [!] Timed out third time, giving up.")
                                import sys
                                sys.exit()


                    except requests.exceptions.ConnectionError:
                        print("      [!] ConnectionError! ")
                        time.sleep(1)

                        try:
                            response = requests.get(url, headers=get_user_agent())
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
                            finished = False
                            # print(row_data)
                            # if row_data.has_attr("aiSosDetailValue"):
                            # print(i)
                            if i == 1:
                                business_type_string = str(row_data.get_text()).upper()
                                print("      [*] Bussiness type: " + business_type_string)
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
                                    business_info["corp_id"] = corp_padded
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
                                finished = True
                    if finished:
                        break


                    # break

                except AttributeError:
                    pass
    except KeyboardInterrupt:
        raise KeyboardInterruptError()
def alabama_scraper_proxy(lists):
    import requests
    from bs4 import BeautifulSoup
    import usaddress
    import csv
    import os
    import time
    from tqdm import tqdm
    from utilities.utilities import get_proxy_cycle, get_open_proxy_cycle
    columns = ["name", "business_types", "state_registered","street_registered","city_registered","zip5_registered", "corp_id"]
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]
    # proxy_cycle = get_proxy_cycle()
    proxy_cycle = get_open_proxy_cycle()
    start_id = lists[0]
    end_id = lists[1]
    file_name = lists[2]
    worker_number = lists[3]
    with open(file_name, "a", encoding="utf-8", newline="") as output_file:
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
                    response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=get_user_agent())
                except TimeoutError:
                    time.sleep(0.9)
                    print("      [!] Timed out")
                    try:
                        response = requests.get(url, proxies={"http": next(proxy_cycle), "https": next(proxy_cycle)}, headers=get_user_agent())
                    except TimeoutError:
                        time.sleep(0.5)
                        print("      [!] Timed out again")

                        try:
                            response = requests.get(url, proxies={"http": next(proxy_cycle), "https": next(proxy_cycle)}, headers=get_user_agent())
                        except TimeoutError:
                            print("      [!] Timed out third time, giving up.")
                            import sys
                            sys.exit()


                except requests.exceptions.ConnectionError:
                    print("      [!] ConnectionError! 1")
                    print("         [*] Proxy: " + str(proxy))
                    time.sleep(1)
                    request_success = False
                    connection_attempts = 0
                    while not request_success or connection_attempts > 10:
                        try:

                            proxy = next(proxy_cycle)
                            print(proxy)
                            response = requests.get(url, proxies={"http": next(proxy_cycle), "https": next(proxy_cycle)}, headers=get_user_agent())
                            request_success = True

                        except requests.exceptions.ConnectionError as e:
                            print(e)
                            time.sleep(1)
                            print("      [!] ConnectionError! 2")
                            print("         [*] Proxy: " + str(proxy))
                            print("      [!] Worker " + str(worker_number) + " connection failed " + str(connection_attempts) + "time(s)")
                            connection_attempts += 1
                            request_success = False

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
                        finished = False
                        # print(row_data)
                        # if row_data.has_attr("aiSosDetailValue"):
                        # print(i)
                        if i == 1:
                            business_type_string = str(row_data.get_text()).upper()
                            print("      [*] Bussiness type: " + business_type_string)
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
                                business_info["corp_id"] = corp_padded
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
                            finished = True
                if finished:
                    break




                # break

            except AttributeError:
                pass
