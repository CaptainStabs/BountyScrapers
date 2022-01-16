import csv
from tqdm import tqdm
import os
from dateutil import parser
import json
import requests


columns = ["state", "county", "physical_address", "property_type", "book", "page", "sale_price", "sale_date", "property_id", "source_url", "year_built"]
filename = "land_info.csv"

payload={}
headers = {}

for property_id in range(0, 9990956954):
    with open(filename, 'a') as output_csv:
        writer = csv.writer(output_csv, fieldnames=columns)

        if os.path.exists(filename) and os.stat(filename).st_size > 3:
            df = pd.read_csv(filename)
            df_columns = list(df.columns)
            data_columns = ",".join(map(str, df_columns))

            # Get the last row from df
            last_row = df.tail(1)
            # Access the corp_id
            last_id = last_row["property_id"].values[0]
            last_id += 1
        else:
            last_id = 100000
            writer.writeheader()


        url = f"https://property.spatialest.com/nc/orange/api/v1/recordcard/{property_id}"
        response = requests.request("GET", url, headers=headers, data=payload)
        cleaned_response = str(response.text).replace("\\", "").strip('"')
        json_data = json.loads(cleaned_response)

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


        if sale_data["seller_name"] != "null":
            land_info["seller_name"] = sale_data["seller_name"]

        if sale_data["SalePrice"] != "null":
            # save
            land_info["sale_price"] = sale_data["SalePrice"]




        # print(json.dumps(json_data, indent=2))
        print(sale_date)


if __name__ == '__main__':
    scraper = Scraper()
    # scraper.main_scraper(filename, columns)
    arguments = []

    # Total divided by 60
    end_id = 9000000
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(10):
        if i == 0:
            start_num = 0
        else:
            # Use end_id before it is added to
            start_num = end_id - 9000000
        print("Startnum: " + str(start_num))
        arguments.append((f"./files/pa_{i}.csv", start_num, end_id))
        end_id = end_id + 1500000
    print(arguments)
    try:
        pool = Pool(processes=10)
        pool.starmap(scraper.main_scraper, arguments, 10)
    except Exception as e:
        print(e)
        tb.print_exc()
        pool.terminate()
        pool.join()
