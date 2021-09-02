from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import pandas as pd
from doltpy.cli.write import write_pandas
from tqdm import tqdm
import time
import usaddress
import csv
import os
from random import randrange
from _secrets import binary_path

class WebDriver:

    location_data = {}

    def __init__(self):
        self.PATH = "C:\\chromedriver_win32\\chromedriver.exe"
        self.options = Options()
        self.options.binary_location = binary_path
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        # self.location_data["location"] = "NA"

    def get_location_data(self):
        global found_address
        try:
            # avg_rating = self.driver.find_element_by_class_name("section-star-display")
            # total_reviews = self.driver.find_element_by_class_name("section-rating-term")
            try:
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'pane')))
                print(element)
            except Exception as e1:
                print("Webdriverwait error: " + str(e1))

            found = False
            times_looped = 0
            while not found and times_looped < 1000:
                try:
                    address = self.driver.find_element(By.XPATH,'/html/body/jsl/div[3]/div[10]/div[8]/div/div[1]/div/div/div[7]/div[1]/button/div[1]/div[2]/div[1]')
                    print(times_looped)
                    found = True
                except Exception as e2:
                    # print("Address find_element error: " + str(e2))
                    found = False
                    times_looped += 1

            if not address.text:
                found = False
                times_looped = 0
                while not found and times_looped < 1000:
                    try:
                        address = self.driver.find_element(By.XPATH,'/html/body/jsl/div[3]/div[10]/div[8]/div/div[1]/div/div/div[7]/div[1]/button/div[1]/div[2]/div[1]')
                        print(times_looped)
                        found = True
                    except Exception as e2:
                        # print("Address find_element error: " + str(e2))
                        found = False
                        times_looped += 1

                if not address.text:
                    print("Not found address")
                    found_address = False
                else:
                    print("Found address")
                    found_address = True
            else:
                found_address = True

            # phone_number = self.driver.find_element_by_css_selector("[data-tooltip='Copy phone number']")
            website = self.driver.find_element_by_css_selector("[data-item-id='authority']")

        except Exception as e:
            print("First block: " + str(e))
            pass
        try:
            # self.location_data["rating"] = avg_rating.text
            # self.location_data["reviews_count"] = total_reviews.text[1:-1]
            self.location_data["location"] = address.text
            # self.location_data["contact"] = phone_number.text
            self.location_data["website"] = website.text
        except Exception as E:
            print("Second block: " + str(E))
            pass

    def scrape(self, url):
        print("Scraping")
        input_source = "schools.csv"
        df = pd.read_csv(input_source)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))
        columns = ["name","city","state","address","zip"]

        with open("address_updated.csv", "a") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=columns)
            if os.stat("address_updated.csv").st_size == 0:
                writer.writeheader()

            for index, row in tqdm(df.iterrows()):
                print("Iterating")
                school_info = {}
                school_name = row["name"]
                school_city = row["city"]
                school_state = row["state"]
                search_query = f"{school_name}, {school_city}, {school_state}"
                print("\nSearch query: " + str(search_query))


                try:
                    self.driver.get(url)
                except Exception as e:
                    print("Scrape error 1: " + str(e))
                    self.driver.quit()
                    pass
                # time.sleep(10)

                searchbox = self.driver.find_element(By.ID,"searchboxinput")
                searchbox.send_keys(search_query)
                searchbox.send_keys(Keys.ENTER)
                # self.click_open_close_time()
                self.get_location_data()

                # time.sleep(2)
                if found_address:
                    print(self.location_data)
                    # return(self.location_data)

                    address_string = self.location_data["location"]
                    address_list = address_string.split(", ")
                    # ['1807 Martin Luther King Jr Way', 'Oakland', 'CA 94612']

                    parsed_address = usaddress.tag(address_string)
                    # ([('AddressNumber', '1807'), ('StreetName', 'Martin Luther King Jr'), ('StreetNamePostType', 'Way'), ('PlaceName', 'Oakland'), ('StateName', 'CA'), ('ZipCode', '94612')]), 'Street Address')

                    street_address = str(address_list[0]).upper()
                    print("Street Address: " + str(street_address))
                    print(address_list)
                    print("parsed_address: " + str(parsed_address))
                    print("Key selection: " + str(parsed_address[0]["AddressNumber"]))
                    parsed_city = str(parsed_address[0]["PlaceName"]).upper()
                    parsed_state = str(parsed_address[0]["StateName"]).upper()
                    parsed_zip = str(parsed_address[0]["ZipCode"])
                    print(parsed_city)
                    print(parsed_state)

                    if parsed_city == str(school_city) and parsed_state == str(school_state):
                        print("Updating Address")
                        school_info["name"] = row["name"]
                        school_info["city"] = row["city"]
                        school_info["state"] = row["state"]
                        school_info["address"] = street_address
                        school_info["zip"] = parsed_zip
                        writer.writerow(school_info)

                        time.sleep(randrange(10))
                else:
                    with open("fails.txt", "a") as f:
                        f.write(f"{school_name}, {school_city}, {school_state}\n")
                    continue







url = "https://www.google.com/maps/"

x = WebDriver()
x.scrape(url)

# for index, row in tqdm(df.iterrows()):
#     school_name = row["name"]
#     school_city = row["city"]
#     school_state = row["state"]
#     search_query = f"{school_name}, {school_city}, {school_state}"
#     print("\nSearch query: " + str(search_query))
#     x = WebDriver()
#     location_data = x.scrape(url, search_query)
#     print(location_data)
#     time.sleep(3)
#
# write_pandas(dolt, "schools")
