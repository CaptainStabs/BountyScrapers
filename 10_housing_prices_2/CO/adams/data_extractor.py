import pandas as pd
import numpy as np
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse
# from _sale_type import sale_type
#
# def deed_translator(x):
#     if x:
#         try:
#             return sale_type[x]
#         except KeyError:
#             return x

df = pd.read_csv('cleaned_combined.csv')

#,"","asdimpsval","asdtotalval","lotsize","lotmeasure"
# bedrooms,baths,exterior,attgarsf,detgarsf,bsmntsf,finbsmntsf,pin
df.rename(columns={
    "PARCELNB": "property_id",
    "CONCATADDR1": "property_street_address",
    "LOCCITY": "property_city",
    "LOCZIP":  "property_zip5",
    "deedtype": "transfer_deed_type",
    "salesp": "sale_price",
    "grantor": "seller_1_name",
    "grantee": "buyer_1_name",
    "accttype": "land_type",
    "actlandval": "land_appraised_value",
    "actimpsval": "building_appraised_value",
    "acttotalval": "total_appraised_value",
    "asdlandval": "land_assessed_value",
    "asdimpsval": "building_assessed_value",
    "asdtotalval": "total_assessed_value",
    "proptype": "property_type",
    "yrblt": "building_year_built",
    "sf": "building_area_sqft",
    "bedrooms": "building_num_beds",
    "baths": "building_num_baths",
    "saledt": "sale_datetime"
}, inplace=True)

df["building_year_built"] = np.where(df["building_year_built"] > 0, df["building_year_built"], pd.NA)

df["land_area_acres"] = np.where((df["lotmeasure"] == "Acres"), df["lotsize"], pd.NA)
df["land_area_sqft"] = np.where((df["lotmeasure"] == "SF"), df["lotsize"], pd.NA)
df["source_url"] = df["property_id"].apply(lambda x: f"https://gisapp.adcogov.org/QuickSearch/doreport.aspx?pid=0{x}")

df["state"] = "CO"
df["property_county"] = "ADAMS"

# df["sale_datetime"] = pd.to_datetime(df["sale_datetime"])
df["sale_datetime"] = df["sale_datetime"].apply(lambda x: date_parse(x))
df["page"] = df["page"].apply(lambda x: x.split("-")[0] if type(x) == str else x)

df = df.dropna(subset='property_street_address', axis=0)

# df["transfer_deed_type"] = df["transfer_deed_type"].apply(lambda x: deed_translator(x))

# 'lotsize',
#        'lotmeasure', 'bltasdesc', 'rooms',

df = df.drop(["lotsize", "lotmeasure", "bltasdesc", "rooms", "land_assessed_value", "building_assessed_value", "total_assessed_value"], axis=1)

df.to_csv("extracted_data.csv", index=False)
