import requests
from lxml.html import fromstring
import csv
import pandas as pd
from utils.business_parser import business_type_parser
import os
import usaddress
from tqdm import tqdm
from multiprocessing import Pool




filename = "pa.csv"

class Scraper():
    def __init__(self):
        self.headers = headers = {
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document'
        }
        self.url = "https://www.corporations.pa.gov/search/corpsearch"
        self.columns = ["name", "business_type", "state_registered", "street_registered", "city_registered", "zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "agent_name", "agent_title", "raw_physical_address", "raw_registered_address"]

        # main_scraper(self, filename, columns)

    # Get last id from csv to pick up where left off
    def get_last_id(self, filename):
        if os.path.exists(filename) and os.stat(filename).st_size > 0:
            df = pd.read_csv(filename)
            df_columns = list(df.columns)
            data_columns = ",".join(map(str, df_columns))

            # Get the last row from df
            last_row = df.tail(1)
            # Access the corp_id
            last_id = last_row["filing_number"].values[0]
            last_id += 1
            return last_id
        else:
            last_id = 1
            return last_id

    # Step two
    def get_result_page(self, s, corp_id):
        # Setup payload
        payload = {
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': self.event_validation,
            '__VIEWSTATE': self.view_state,
            'ctl00$MainContent$btnSearch': 'Search',
            'ctl00$MainContent$ddlSearchType': '1',
            'ctl00$MainContent$txtSearchTerms': corp_id,
            'ctl00$MainContent$ddlSearchType': '6' # Exact match search
        }

        # Get "Select Business Entity page"
        result_page = s.request("POST", self.url, data=payload)

        # Get view stuff from this page, and buttons daat
        self.result_parser = fromstring(result_page.text)

        # Get aspx junk for step 2 request
        self.event_validation_2 = self.result_parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        self.view_state_2 = self.result_parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

    def request_business_info(self, s, tries=0):
        '''
        Step 2:
        After searching, we need to get the view_state and event_validation once again
        EVENTTARGET is from the result list link pointing to entity name
        This step (finally) gets the actual business info
        '''

        payload = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ctl00$MainContent$gvResults$ctl02$lnkBEName',
            '__EVENTVALIDATION': self.event_validation_2,
            '__VIEWSTATE': self.view_state_2
        }


        business_page = s.request("POST", self.url, headers=self.headers, data=payload)
        self.business_parser = fromstring(business_page.text)

        try:
            self.df = pd.read_html(business_page.text)
            entity_details = self.df[1]
            # print(entity_details)
            self.info_dict = entity_details.set_index(0).to_dict()
        except IndexError:
            print("      [!] No tables found, trying connection again")
            if tries < 5:
                self.request_business_info(s, tries)
                tries += 1

    def main_scraper(self, filename, last_id):
        with open(filename, "a", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.columns)

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            s = requests.Session()
            s.headers.update(self.headers)

            for corp_id in tqdm(range(self.get_last_id(filename), last_id)):
                print(f"   [*] Current ID: {corp_id}")
                '''
                Step 1:
                Need to get the first search page to search for ID
                '''

                # Get search page
                response = s.request("GET", self.url, headers=self.headers)

                # Parse raw html with lxml
                parser = fromstring(response.text)

                self.event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                self.view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

                self.get_result_page(s, corp_id)

                try:
                    business_status = str(self.result_parser.xpath('//*[@id="lblBEStatus"]/text()')[0]).upper().strip()
                    got_results = True
                except IndexError:
                    # This is caused by no results being returned
                    print("      [!] Business status not found!")
                    got_results = False

                # Prevent rest of script from running
                if got_results:
                    # Only want active businesses
                    if business_status == "ACTIVE":
                        self.request_business_info(s)

                        self.business_info = {
                            "name": " ".join(str(self.business_parser.xpath('//td[@align="left"]/text()')[0]).strip().upper().split()),
                            "business_type": "CORPORATION", # This will get replaced if it is parsed
                            "state_registered": str(self.info_dict[1]["State Of Inc"]).upper().strip(),
                            "filing_number": str(self.info_dict[1]["Entity Number"]).strip()
                            }

                        print("      [*] Name: " + str(self.business_parser.xpath('//td[@align="left"]/text()')[0]).strip())



                        """Parse physical address"""

                        raw_physical_address = str(self.info_dict[1]['Address']).upper().strip()
                        print(f"   [*] Physical Address: {raw_physical_address}")
                        self.business_info["raw_physical_address"] = raw_physical_address

                        try:
                            parsed_address = usaddress.tag(raw_physical_address)
                            parse_success = True

                        except usaddress.RepeatedLabelError as e:
                            print(e)
                            parse_success = False


                        if parse_success:
                            print(parsed_address)

                            try:
                                street_physical = " ".join(str(raw_physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip().upper().split())
                                self.business_info["street_physical"] = street_physical
                            except KeyError:
                                print("         [!] Physical PlaceName was not parsed!")

                            try:
                                self.business_info["city_physical"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().upper().split())

                            except KeyError:
                                print("         [!] City physical key error!")

                            try:
                                self.business_info["zip5_physical"] = str(parsed_address[0]["ZipCode"]).strip()

                            except KeyError:
                                print("         [!] Physical Zip code key error!")

                            try:
                                self.business_info["state_physical"] = str(parsed_address[0]["StateName"]).upper().strip()
                            except KeyError:
                                print("         [!] State physical key error!")

                        # Registered agent will need a check to see if officer table exists
                        if len(self.df) == 6:
                            agent_details = self.df[2]
                            agent_dict = agent_details.set_index(0).to_dict()

                            try:
                                self.business_info["agent_name"] = str(agent_dict[1]["Name"]).upper().strip()
                                self.business_info["agent_title"] = str(agent_dict[1]["Title"]).upper().strip()

                            except KeyError:
                                print("      [!] Agent name or agent title key error!")

                            raw_registered_address = " ".join(str(agent_dict[1]["Address"]).split()).upper().strip()

                            print(f"   [*] Agent address: {raw_registered_address}")
                            if raw_registered_address != "NAN":
                                self.business_info["raw_registered_address"] = raw_registered_address
                                try:
                                    parsed_registered_address = usaddress.tag(raw_registered_address)
                                    parse_success = True
                                except usaddress.RepeatedLabelError as e:
                                    print("      [!] Registered address parsing failed!\n      " + str(e))
                                    parse_success = False

                                if parse_success:
                                    try:

                                        street_registered = str(raw_registered_address).split(parsed_registered_address[0]["PlaceName"])[0]
                                        street_registered = street_registered.strip(",").strip().upper()
                                        self.business_info["street_registered"] = street_registered
                                    except KeyError:
                                        print("         [!] Registered PlaceName parse failed!")

                                    try:
                                        self.business_info["city_registered"] = " ".join(str(parsed_registered_address[0]["PlaceName"]).strip(",").strip().upper().split())
                                    except KeyError:
                                        print("         [!] City Registered parse failure!")

                                    try:
                                        self.business_info["zip5_registered"] = str(parsed_address[0]["ZipCode"]).strip()

                                    except KeyError:
                                        print("         [!] zip5_registered parse failure!")

                            else:
                                print("      [!] Raw registered address is nan, skipping.")



                        business_type_string = self.info_dict[1]["Entity Type"]
                        self.business_info["business_type"] = business_type_parser(str(business_type_string).upper().strip())

                        writer.writerow(self.business_info)

                    else:
                        print(f"      [!] Business not active: {business_status}")
if __name__ == '__main__':
    scraper = Scraper()
    # scraper.main_scraper(filename, columns)
    pool = Pool(processes=100)
    pool.starmap(scraper.main_scraper(filename, last_id))
