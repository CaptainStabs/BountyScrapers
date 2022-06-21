import pandas as pd
import json

def year_validator(x):
    if x:
        if "-" in x:
            return x.split('-')[0]
        else:
            return x


with open("objects.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    data = data["data"]

df = pd.DataFrame.from_dict(data)

df["object_number"] = df["uri"].apply(lambda x: x[9:])
df["source_1"] = df["uri"].apply(lambda x: "https://api.rockarch.org" + x)
df["date_description"] = df["dates"].apply(lambda x: x[0]['expression'])
df["year_start"] = df["dates"].apply(lambda x:  year_validator(x[0]['begin']))
df["year_end"] = df["dates"].apply(lambda x:  year_validator(x[0]['end']))
df["date_description"] = df["date_description"].replace("undated", pd.NA)
df.drop(["type", "uri", "dates"], axis=1, inplace=True)

df["institution_name"] = "Rockefeller Archive Center"
df["institution_city"] = "Sleepy Hollow"
df["institution_state"] = "New York"
df["institution_country"] = "United States"
df["institution_latitude"] = 41.0919742529525
df["institution_longitude"] = -73.83528113087031

df.to_csv("extracted_data.csv", index=False)
