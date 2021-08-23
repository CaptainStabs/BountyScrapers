import requests
import urllib
import os
import pandas as pd
import time
from _secrets import here_key, here_oauth

headers = {
    'Authorization': f'Bearer {here_oauth}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Content-Type': 'gzip',
    'Accept': 'application/json',
}

api_endpoint = "https://geocode.search.hereapi.com/v1/geocode?q="

with open("addresses_HIFLD_Schools.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    with open("addresses_updated.csv", "a", encoding="utf-8") as output_file:
        for index, row in df.iterrows():


            name = row["name"]
            city = row["city"]
            state = row["state"]
            country = row["COUNTRY"]

            query = f"{name} {city} {state} {country}"
            query_encoded = urllib.parse.quote_plus(query)
            print(query_encoded)

            search_query = api_endpoint + query_encoded +f"&apiKey={here_key}"

            response = requests.request("GET", search_query, headers=headers)
            print(response.json)
            print(response.text)
            time.sleep(0.2)
            break
