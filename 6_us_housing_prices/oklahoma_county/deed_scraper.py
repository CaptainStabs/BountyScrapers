import requests
from lxml.html import fromstring
import csv
import pandas as pd
import os
import usaddress
from tqdm import tqdm
from multiprocessing import Pool
import traceback as tb
# from datetime import datetime
from dateutil import parser as dateparser
import time

import heartrate; heartrate.trace(browser=True, daemon=True)

class KeyboardInterruptError(Exception):
    pass

class Scraper():
    def __init__(self):
        self.headers = {
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Cookie': 'ASPSESSIONIDSQQAARDC=OLCJBOCALPJEDCDIOGHEIJEN'
        }

        self.columns = ["state", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "year_built", "source_url", "book", "page", "type", "prop_id"]

    def get_last_id(self, filename):
        if os.path.exists(filename) and os.stat(filename).st_size > 0:
            df = pd.read_csv(filename)
            df_columns = list(df.columns)
            data_columns = ",".join(map(str, df_columns))

            # Get the last row from df
            last_row = df.tail(1)
            # Access the corp_id
            last_id = last_row["prop_id"].values[0]
            last_id += 1
            return last_id
        else:
            last_id = 1
            return last_id

    def main_scraper(self, filename, start_num, end_id):
        try:
            with open(filename, "a", encoding="utf-8", newline="") as output_file:
                writer = csv.DictWriter(output_file, fieldnames=self.columns)

                if os.path.exists(filename) and os.stat(filename).st_size > 0:
                    start_id = self.get_last_id(filename)
                else:
                    start_id = start_num

                if os.stat(filename).st_size == 0:
                    writer.writeheader()

                s = requests.Session()
                s.headers.update(self.headers)


                for prop_id in tqdm(range(start_id, int(end_id))):
                    url = f"https://docs.oklahomacounty.org/AssessorWP5/AN-R.asp?PropertyID={prop_id}"

                    request_success = False
                    request_tries = 0
                    while not request_success or request_tries > 10:
                        try:
                            # Get search page
                            response = s.request("GET", url, headers=self.headers)
                            request_success = True
                        except requests.exceptions.ConnectionError:
                            print("  [!] Connection Closed! Retrying in 1...")
                            time.sleep(1)
                            # response = requests.request("GET", url, headers=get_user_agent(), data=payload)
                            request_success = False

                    if request_success:
                        land_info = {
                            "state": "OK",
                            "county": "OKLAHOMA",
                            "source_url": url,
                            "prop_id": prop_id
                        }

                        parser = fromstring(response.text)

                        # "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "year_built", "source_url", "book", "page"]
                        try:
                            physical_address = " ".join(str(parser.xpath('/html/body/table[4]/tbody/tr[1]/td[5]/p/font/text()')[0]).strip().lstrip("\r\n\t\t\t").upper().split())
                            if physical_address != "UNKNOWN" and physical_address != "0 UNKNOWN" and physical_address != "0" and physical_address != "0 0":
                                land_info["physical_address"] = physical_address
                        except IndexError as e:
                            # print("PHYSICAL_ADDRESS", e)
                            pass

                        try:
                            city = " ".join(str(parser.xpath('/html/body/table[4]/tbody/tr[2]/td[4]/p/font/text()')[0]).strip().lstrip("\r\n\t\t\t").upper().split())

                            if city and city != "UNINCORPORATED":
                                land_info["city"] = city

                            else:
                                land_info["city"] = ""
                        except IndexError as e:
                            # print("CITY", e)
                            pass

                        try:
                            land_info["property_id"] = " ".join(str(parser.xpath('/html/body/table[4]/tbody/tr[1]/td[1]/font/font/text()')[0]).strip().lstrip("\r\n\t\t\t").upper().split())
                        except IndexError as e:
                            # print("PROPERTY_ID", e)
                            pass

                        table = parser.xpath('//table[./thead/tr/th/font/text()="\r\n\t\t\tProperty Deed Transaction History\xa0\xa0 ("]/tbody/tr')
                        for row in table:
                            # print(str(row.xpath('./td[1]/p/font/text()')[0]).lstrip("\r\n\t\t\t"))

                            try:
                                land_info["sale_date"] = dateparser.parse(str(row.xpath('./td[1]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip())  + " 00:00:00")
                            except IndexError as e:
                                # print("Sale date", e)
                                pass

                            try:
                                land_info["type"] = str(row.xpath('./td[3]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip()).upper()
                            except IndexError as e:
                                # print("Type", e)
                                pass

                            try:
                                land_info["book"] = str(row.xpath('./td[4]/p/font/a/text()')[0].lstrip("\r\n\t\t\t").strip())
                            except IndexError as e:
                                # print("Book", e)
                                pass

                            try:
                                land_info["page"] = str(row.xpath('./td[5]/p/font/a/text()')[0].lstrip("\r\n\t\t\t").strip())
                            except IndexError as e:
                                # print("page", e)
                                pass

                            try:
                                land_info["sale_price"] = str(row.xpath('./td[6]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip()).replace(",", "")
                            except IndexError as e:
                                # print("Price", e)
                                pass

                            try:
                                land_info["seller_name"] = " ".join(str(row.xpath('./td[5]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip()).split()).upper()
                            except IndexError as e:
                                # print("Seller Name", e)
                                pass

                            try:
                                land_info["buyer_name"] = " ".join(str(row.xpath('./td[6]/p/font/text()')[0].lstrip("\r\n\t\t\t").strip()).split()).upper()
                            except IndexError as e:
                                # print("Buyer Name", e)
                                pass

                            try:
                                land_info["year_built"] = str(parser.xpath('//table[./thead/tr/th/font/text()="Click \r\n\t\t\tbutton on building number to access \r\n\t\t\tdetailed information:"]/tbody/tr/td[5]/p/font/text()')[0].strip("\r\n\t\t\t").strip())
                            except IndexError as e:
                                # print("Yearbuilt", e)
                                pass

                            # Each deed needs to be written
                            writer.writerow(land_info)








        except Exception as e:
            print(e)

if __name__ == '__main__':
    scraper = Scraper()
    # scraper.main_scraper(filename, columns)
    arguments = []

    # Total divided by 60
    end_id = 9000000
    # start_num is supplemental for first run and is only used if the files don't exist
    # for i in range(10):
    #     if i == 0:
    #         start_num = 0
    #     else:
    #         # Use end_id before it is added to
    #         start_num = end_id - 9000000
    #     print("Startnum: " + str(start_num))
    #     arguments.append((f"./files/deeds_{i}.csv", start_num, end_id))
    #     end_id = end_id + 1500000
    # print(arguments)

    scraper.main_scraper("./files/deeds_0.csv", 200000, 354299)

    # try:
    #     pool = Pool(processes=1)
    #     pool.starmap(scraper.main_scraper, arguments, 1)
    #
    # except KeyboardInterrupt:
    #     print("Quitting")
    #     pool.terminate()
    # except Exception as e:
    #     print(e)
    #     tb.print_exc()
    #     pool.terminate()
    # finally:
    #     print("   [*] Joining pool...")
    #     pool.join()
    #     print("   [*] Finished joining...")
    #     # sys.exit(1)
