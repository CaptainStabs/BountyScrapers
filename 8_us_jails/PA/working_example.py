import functools
import usaddress
import logging
import polars as pl
import pandas as pd
import os
import secrets
import numpy as np
from tqdm import tqdm; tqdm.pandas()

# Parse jail address and create/append the parsed data to a new file to import into jails
@functools.lru_cache(maxsize=None)
def parse_address(jail_name, state, county, address, file, verbosity):
    if "N/A" not in address:
        address_dict = {"id": "STABS" + str(secrets.token_hex(16)), "county": county, "facility_name": jail_name, "facility_address": None, "facility_city": None,  "facility_state": state, "facility_zip": None, "is_private":0, "in_urban_area": 0, "holds_greater_than_72_hours": -9, "holds_less_than_1_yr": -9, "felonies_greater_than_1_yr": -9, "holds_greater_than_1_yr": -9, "hold_less_than_72_hours": -9, "facility_gender": 1, "num_inmates_rated_for": 0}
        dtype = {"id":str,
                "facility_zip":str,
                "is_private": int,
                "in_urban_area": int,
                "holds_greater_than_72_hours": int,
                "holds_less_than_1_yr": int,
                "felonies_greater_than_1_yr": int,
                "holds_greater_than_1_yr":int,
                "hold_less_than_72_hours":int,
                "facility_gender":int,
                "num_inmates_rated_for":int
                }
        if not os.path.exists(file):
            header = True
            df = pl.from_pandas(pd.DataFrame(columns=["id","county","facility_name","facility_address","facility_city","facility_state","facility_zip","is_private","in_urban_area","holds_greater_than_72_hours","holds_less_than_1_yr","felonies_greater_than_1_yr","holds_greater_than_1_yr","hold_less_than_72_hours","facility_gender","num_inmates_rated_for"], dtype=int))

        elif os.path.exists(file) and os.stat(file).st_size > 271:
            df = pl.read_csv(file, has_header=True, dtype=dtype)
            header = False
        else:
            header = True
            df = pl.from_pandas(pd.DataFrame(columns=["id","county","facility_name","facility_address","facility_city","facility_state","facility_zip","is_private","in_urban_area","holds_greater_than_72_hours","holds_less_than_1_yr","felonies_greater_than_1_yr","holds_greater_than_1_yr","hold_less_than_72_hours","facility_gender","num_inmates_rated_for"], dtype=str))

        raw_address = str(address).upper().strip()
        try:
            parsed_address = usaddress.tag(raw_address)
            parse_success = True
        except usaddress.RepeatedLabelError as e:
            parse_success = False
            logging.warning(e)

        if parse_success:
            try:
                address_dict["facility_address"] = " ".join(str(raw_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip().split())
            except usaddress.RepeatedLabelError as e:
                logging.warning(e)

            try:
                address_dict["facility_city"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().split())
            except KeyError:
                logging.warning("  [!] City key error!")

            try:
                address_dict["facility_zip"] = str(parsed_address[0]["ZipCode"]).strip()

            except KeyError:
                logging.warning("   [!] Zip key error")

            adl = list(address_dict.items())
            # print(address_dict.values())
            df = df.to_pandas()
            # Append the parsed data to the dataframe
            df2 = pd.DataFrame(address_dict.values(), dtype=str)

            # print(df)
            df2 = pl.from_pandas(df2)
            df2 = df2.transpose(include_header=False, column_names=address_dict.keys())

            df = pd.concat([df, df2.to_pandas()])
            df = df.drop_duplicates(subset=["id""facility_name", "facility_address", "county"])


            if header:
                df.to_csv(file, mode="a", index=False)
            else:
                df.to_csv(file, mode="a", index=False, header=False)

            return address_dict["id"]

df = pl.read_csv('input_data.csv', has_header=True, null_values="N/A")
df.drop(["Fiscal Year", "Institution Type"])
df = df[df.Institution != "In Federal Prisons"]
df = df[df.Institution != "In County Prisons"]

df = df.to_pandas()
# x = df.iloc[0]
# print(df)
df["id"] = df.progress_apply(lambda x: parse_address(x["Institution"], state="PA", county=x["County"], address=x["Address + Lat/Long"], file="added_jails.csv", verbosity=20), axis=1)
