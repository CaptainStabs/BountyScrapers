from ms_scraper import get_info, get_ids
import pandas as pd
from tqdm import tqdm
import csv



filename = "mississippi_2.csv"
df = pd.read_csv(filename)
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

# Get the last row from df
# last_row = df.tail(1)
# # Access the corp_id
# last_id = last_row["corp_id"].values[0]
# last_id += 1
last_id =  1192315

columns = ["name", "business_type", "state_registered","street_physical","city_physical","zip5_physical", "filing_number", "corp_id"]
notify_url = "https://notify.run/c/pBglF5lgM2GWUsRV"

for i in range(4):
        try:
            with open(filename, "a", encoding="utf-8", newline="") as output_file:
                writer = csv.DictWriter(output_file, fieldnames=columns)

                if os.stat(filename).st_size == 0:
                    writer.writeheader()

                # business_id = 1073778                1975860
                for business_id in tqdm(range(last_id, 1975860)):
                    print("\n   [*] Current id: " + str(business_id))
                    try:
                        get_info(get_ids(business_id), writer)
                    except Exception as e:
                        with open("fail_1.txt", "a", newline="") as fail_file:
                            fail_file.write(str(e))
                            message_data = f"Your district scrpaer crashed. Error: \n{str(e)}"
                            response = requests.post(notify_url, data=message_data)
        except Exception as e:
            with open("fail_2.txt", "a", newline="") as fail_file:
                fail_file.write(str(e))
                message_data = f"Your district scrpaer crashed. Error: \n{str(e)}"
                response = requests.post(notify_url, data=message_data)
