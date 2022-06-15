from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import pandas as pd
# from doltpy.cli.write import write_pandas
from tqdm import tqdm
import time
import usaddress
import csv
import os
from random import randrange
# from _secrets import binary_path
import argparse
# import heartrate; heartrate.trace(browser=True, daemon=True)
import secrets
import sys

def cli():
    parser = argparse.ArgumentParser(description='Download binary files')
    parser.add_argument('--file', type=str, default= "jails.csv", help='Path to file')
    parser.add_argument('--state', type=str, help='Facility state')
    parser.add_argument("--col_name", type=str, default="name", help='Column name containing the facility name')
    parser.add_argument("--col_capacity", type=str, default="capacity", help='Column name for capacity')
    parser.add_argument("--add_jail", action='store_const', const=True, help='Whether to append jail to search')
    parser.add_argument("--binary_path", type=str, default="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", help="Path to chrome binary")
    parser.add_argument("--driver_path", type=str, default="C:\\chromedriver_win32\\chromedriver.exe", help="Path to chrome driver")
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    url = "https://www.google.com/maps/"

    x = WebDriver(args)
    x.scrape(url, args)


class WebDriver:
    location_data = {}

    def __init__(self, args):
        self.PATH = args.driver_path
        self.options = Options()
        self.options.binary_location = args.binary_path
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        # self.location_data["location"] = "NA"

        self.found_address = False

    def get_location_data(self):
        # global found_address
        try:
            # avg_rating = self.driver.find_element_by_class_name("section-star-display")
            # total_reviews = self.driver.find_element_by_class_name("section-rating-term")
            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'pane')))
                # print(element)
            except Exception as e1:
                print("   [!] Webdriverwait error: " + str(e1))

            found = False
            times_looped = 0
            time.sleep(1.5)
            while not found and times_looped < 1000:
                try:
                    address = self.driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[7]/div[1]/button/div[1]/div[2]/div[1]').text
                    # address_2 = self.driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span')
                    # address = str(address_1.text) +  ", " + str(address_2.text)
                    print("   [*] times_looped: " + str(times_looped))
                    found = True
                except Exception as e2:
                    # print("Address find_element error: " + str(e2))
                    found = False
                    times_looped += 1

            if address is None:
                print("Not address.text: " + str(address))
                found = False
                times_looped = 0
                time.sleep(5)
                while not found and times_looped < 1000:
                    try:
                        address = self.driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[7]/div[1]/button/div[1]/div[2]/div[1]').text
                        # address_2 = self.driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span')
                        # address = str(address_1.text) +  ", " + str(address_2.text)
                        print(address)
                        print("   [*] times_looped: " + str(times_looped))
                        found = True
                    except Exception as e2:
                        # print("Address find_element error: " + str(e2))
                        found = False
                        times_looped += 1

                if address is None:
                    print("   [?] Not found address")
                    self.found_address = False
                else:
                    print("   [?] Found address")
                    print("      [*] Address: " + str(address))
                    self.found_address = True
            else:
                print("      [*] Found Address")
                print("      [*] Address: " + str(address))
                self.found_address = True

            # phone_number = self.driver.find_element_by_css_selector("[data-tooltip='Copy phone number']")
            # website = self.driver.find_element_by_css_selector("[data-item-id='authority']")

        except Exception as e:
            print("   [!] First block: " + str(e))
            self.found_address = False
            pass
        try:
            # self.location_data["rating"] = avg_rating.text
            # self.location_data["reviews_count"] = total_reviews.text[1:-1]
            self.location_data["location"] = address
            # self.location_data["contact"] = phone_number.text
            # self.location_data["website"] = website.text
        except Exception as E:
            print("   [!]Second block: " + str(E))
            pass


    def scrape(self, url, args):
        print("Scraping")
        input_source = args.file
        df = pd.read_csv(input_source)
        with open(input_source, "r", encoding="utf-8") as f:
            total = 0
            lines = f.readlines()
            print(len(lines))
            for line in lines:
                total += 1
            print(total)

        with open("address_updated.csv", "a", encoding="utf-8") as output_file:
            columns = ["id","facility_name", "facility_address", "facility_city","facility_state", "facility_zip", "is_private", "in_urban_area", "holds_greater_than_72_hours",
            "holds_less_than_1_yr","felonies_greater_than_1_yr", "hold_less_than_72_hours","facility_gender","num_inmates_rated_for"]
            writer = csv.DictWriter(output_file, fieldnames=columns)
            if os.stat("address_updated.csv").st_size == 0:
                writer.writeheader()

            # with open("other_addresses.csv", "a") as other_output:
            #     writer2 = csv.DictWriter(other_output, fieldnames=columns)
            # if os.stat("other_addresses.csv").st_size == 0:
            #     writer2.writeheader()

            for index, row in tqdm(df.iterrows(), total=total):
                print("Iterating")
                name = row[args.col_name]
                physical_state = args.state
                if args.add_jail:
                    search_query = f"{name} Jail, {physical_state}"
                else:
                    search_query = f"{name}, {physical_state}"
                print("\n   [?] Search query: " + str(search_query))

                try:
                    self.driver.get(url)
                except Exception as e:
                    print("   [!] Scrape error 1: " + str(e))
                    self.driver.quit()
                    pass
                # time.sleep(10)

                searchbox = self.driver.find_element(By.ID,"searchboxinput")
                searchbox.send_keys(search_query)
                searchbox.send_keys(Keys.ENTER)
                # self.click_open_close_time()
                self.get_location_data()

                # time.sleep(2)
                if self.found_address:
                    # print("     [?] Location Data: " + str(self.location_data))
                    # return(self.location_data)

                    address_string = self.location_data["location"]
                    print(address_string)
                    address_list = address_string.split(", ")
                    # ['1807 Martin Luther King Jr Way', 'Oakland', 'CA 94612']
                    try:
                        parsed_address = usaddress.tag(address_string)
                        parse_success = True
                    except usaddress.RepeatedLabelError as e:
                        new_address = address_string
                        with open("fails2.txt", "a") as output:
                            old_address = row[args.col_name]
                            output.write(f"{address_string}, {physical_city}, {physical_state}, {old_address}, {new_address}\n")
                            parse_success = False


                    # ([('AddressNumber', '1807'), ('StreetName', 'Martin Luther King Jr'), ('StreetNamePostType', 'Way'), ('PlaceName', 'Oakland'), ('StateName', 'CA'), ('ZipCode', '94612')]), 'Street Address')
                    if parse_success:
                        street_address = str(address_list[0])
                        print("      [?] Street Address: " + str(street_address))
                        # print(address_list)
                        # print("      [?] parsed_address: " + str(parsed_address))
                        # print("      [?] Key selection: " + str(parsed_address[0]["AddressNumber"]))
                        # print("      [?] New Address: " + str(address_string))
                        try:
                            parsed_city = str(parsed_address[0]["PlaceName"])
                            parsed_state = str(parsed_address[0]["StateName"])
                            parsed_zip = str(parsed_address[0]["ZipCode"])
                            print("      [?] parsed_city: " + str(parsed_city))
                            print("      [?] parsed_state: " + str(parsed_state))
                            parse_success = True
                        except KeyError:
                            print("key error")
                            parse_success = False

                    # except Exception as e:
                    #     print(e)
                    #     new_address = address_string
                    #     with open("fails2.txt", "a") as output:
                    #         output.write(f"{physical_address}, {physical_city}, {physical_state}, {old_address}, {new_address}\n")

                    if parse_success:
                        if parsed_state == str(physical_state):
                            print("   [*] Updating Address")
                            land_info = {
                                "id": "STABS" + str(secrets.token_hex(8)),
                                "facility_name" : row[args.col_name],
                                "facility_address": street_address,
                                "facility_city": parsed_city,
                                "facility_state": args.state,
                                "facility_zip": parsed_zip,
                                "is_private": 0,
                                "in_urban_area": 0,
                                "holds_greater_than_72_hours": -9,
                                "holds_less_than_1_yr": -9,
                                "felonies_greater_than_1_yr": -9,
                                "hold_less_than_72_hours": -9,
                                "facility_gender": 3,
                                "num_inmates_rated_for": str(row[args.col_capacity]).replace(",", "").strip('"')
                            }

                            # land_info["zip5"] = parsed_zip
                            writer.writerow(land_info)

                            # Not in the time.sleep as i want to print the time to see it
                            sleep_time = randrange(5)
                            print("         [*] Sleeping for " + str(sleep_time))
                            time.sleep(sleep_time)

#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Download binary files')
#     parser.add_argument('--file', type=str, default= "jails.csv", help='Path to file')
#     parser.add_argument('--state', type=str, help='Facility state')
#     parser.add_argument("--col_name", type=str, default="name", help='Column name containing the facility name')
#     parser.add_argument("--col_capacity", type=str, default="capacity", help='Column name for capacity')
#     parser.add_argument("--add_jail", action='store_const', const=True, help='Whether to append jail to search')
#     parser.add_argument("--binary_path", type=str, default="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", help="Path to chrome binary")
#     parser.add_argument("--driver_path", type=str, default="C:\\chromedriver_win32\\chromedriver.exe", help="Path to chrome driver")
#     args = parser.parse_args()
#     if len(sys.argv)==1:
#         parser.print_help(sys.stderr)
#         sys.exit(1)
#     url = "https://www.google.com/maps/"
#
#     x = WebDriver(args)
#     x.scrape(url, args)
# for index, row in tqdm(df.iterrows()):
#     physical_address = row["name"]
#     physical_city = row["city"]
#     physical_state = row["state"]
#     search_query = f"{physical_address}, {physical_city}, {physical_state}"
#     print("\nSearch query: " + str(search_query))
#     x = WebDriver()
#     location_data = x.scrape(url, search_query)
#     print(location_data)
#     time.sleep(3)
#
# write_pandas(dolt, "schools")
