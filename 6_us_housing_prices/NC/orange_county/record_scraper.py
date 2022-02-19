import csv
from tqdm import tqdm
import os
from dateutil import parser
import json
import requests
import time
from multiprocessing import Pool
import traceback as tb
import heartrate; heartrate.trace(browser=True, daemon=True, port=9998)
import pandas as pd



filename = "land_info.csv"

payload={}
headers = {}

columns = ["state", "county", "physical_address", "property_type", "book", "page", "sale_price", "sale_date", "property_id", "source_url", "year_built"]


class KeyboardInterruptError(Exception):
    pass


def get_last_id(filename):
    if os.path.exists(filename) and os.stat(filename).st_size > 250:
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["property_id"].values[0]
        last_id += 1
        return last_id
    else:
        last_id = 1
        return last_id

def scraper(filename, start_num, end_num):
    try:
        with open(filename, 'a') as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=columns)

            if os.path.exists(filename) and os.stat(filename).st_size > 250:
                start_id = get_last_id(filename)
            else:
                start_id = start_num

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            for property_id in tqdm(range(start_id, end_num)):

                url = f"https://property.spatialest.com/nc/orange/api/v1/recordcard/{property_id}"

                request_success = False
                request_tries = 0
                while not request_success or request_tries > 20:
                    try:
                        response = requests.request("GET", url, headers=headers, data=payload)

                        if "<title>Too Many Requests</title>" in response.text:
                            print(response.text)
                            print("Too many requests 1")
                            time.sleep(10 + request_tries)
                            request_success = False
                        else:
                            request_success = True


                    except Exception as e:
                        time.sleep(0.5)
                        print(e)
                        request_tries += 1

                cleaned_response = str(response.text).replace("\\", "").strip('"')
                # print(cleaned_response)

                try:
                    json_data = json.loads(cleaned_response)
                except json.decoder.JSONDecodeError:
                    pass
                    print("Too many requests")
                    print(cleaned_response)

                try:
                    json_data["error"]

                except KeyError:

                    parcel = json_data["parcel"]
                    sale_data = parcel["sections"][3][0][0]


                    land_info = {
                        "state": "NC",
                        "county": "ORANGE COUNTY",
                        "sale_date": sale_data["order_0"],
                        "book": sale_data["Book"],
                        "page": sale_data["Page"],
                        "physical_address": parcel["header"]["Street"],
                        "property_id": property_id,
                        "source_url": url,

                    }

                    try:
                        if sale_data["seller_name"] != "null":
                            land_info["seller_name"] = sale_data["seller_name"]

                        if sale_data["SalePrice"] != "null":
                            land_info["sale_price"] = sale_data["SalePrice"]
                            print("saving")
                            writer.writerow(land_info)
                    except KeyError:
                        pass

                    time.sleep(4)


    except KeyboardInterrupt:
        raise KeyboardInterruptError()

    except Exception as e:
        print(e)
        raise
        pass

if __name__ == '__main__':
    scraper("land_info.csv", 9799995346, 9990956954)

# Total is 9990956954

# if __name__ == '__main__':
#     arguments = []
#
#     # Total divided by 5
#     end_id = 38192361
#     # start_num is supplemental for first run and is only used if the files don't exist
#     for i in range(5):
#         if i == 0:
#             start_num = 0
#         else:
#             # Use end_id before it is added to
#             start_num = end_id - 38192361
#         # print("Startnum: " + str(start_num))
#         arguments.append((f"./files/record_{i}.csv", start_num, end_id))
#         end_id = end_id + 38192361
#     # print(arguments)
#     try:
#         pool = Pool(processes=5)
#         pool.starmap(scraper, arguments)
#         pool.close()
#     except KeyboardInterrupt:
#         print("   [!] Caught KeyboardInterrupt! Terminating and joining pool...")
#         pool.close()
#         # pool.join()
#     except IndexError as e:
#         print(e)
#         tb.print_exc()
#         print("   [!] Weird pandas/numpy/multithreadding problem, passing")
#         pass
#     except Exception as e:
#         print(e)
#         # logging.exception(e)
#         tb.print_exc()
#         pool.close()
#         # pool.join()
#     finally:
#         print("   [*] Joining pool...")
#         pool.join()
#         print("   [*] Finished joining...")
