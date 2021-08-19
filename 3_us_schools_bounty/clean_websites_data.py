import csv
import os
import pandas as pd

columns = ["name", "city", "state", "website"]

with open("websites_added.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    with open("cleaned_websites.csv", "a", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)

        with open("dirty_websites.csv", "a", encoding="utf-8") as output2:
            writer2 = csv.DictWriter(output2, fieldnames=columns)
            if os.stat("dirty_websites.csv").st_size == 0:
                writer.writeheader()

            if os.stat("cleaned_websites.csv").st_size == 0:
                writer.writeheader()

            for index, row in df.iterrows():
                if "wikipedia" not in row["website"]:
                    output_dict = {}
                    output_dict["name"] = row["name"]
                    output_dict["city"] = row["city"]
                    output_dict["state"] = row["state"]
                    output_dict["website"] = row["website"]

                    writer.writerow(output_dict)

                elif "mapquest" not in row["website"]:
                    output_dict = {}
                    output_dict["name"] = row["name"]
                    output_dict["city"] = row["city"]
                    output_dict["state"] = row["state"]
                    output_dict["website"] = row["website"]

                    writer.writerow(output_dict)

                else:
                    output_dict = {}
                    output_dict["name"] = row["name"]
                    output_dict["city"] = row["city"]
                    output_dict["state"] = row["state"]
                    output_dict["website"] = ""

                    writer2.writerow(output_dict)
