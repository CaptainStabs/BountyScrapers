import pandas as pd
from dateutil import parser
import sys
from pathlib import Path
from tqdm import tqdm

tqdm = tqdm.pandas()

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse


df = pd.read_csv("aug_22.csv", dtype={"STR_PFX": str, "STR_UNIT": str, "ZIP": str, "YR_BLT": str})

df["source_url"] = "https://www.coj.net/departments/property-appraiser/information-offerings/2022-august-re-tr-file-uncertified-access-form.aspx"
df["state"] = "FL"

df.rename(columns={
"STRAP":"property_id",
"SALE_ID": "sale_id",
"GRANTOR": "seller_1_name",
"OR_BK": "book",
"OR_PG": "page",
"DSCR": "sale_type",
"DOS": "sale_datetime",
"PRICE": "sale_price",
"ASD_VAL": "assessed_total",
"BLD_VAL": "building_assessed_value",
"SQFT": "land_area_sqft",
"ACREAGE": "land_area_acreage",
"CITY": "property_city",
"ZIP": "property_zip5",
"YR_BLT": "building_year_built",
"00001 Parcel_DSCR": "property_type"
}, inplace=True)

df[["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT"]] = df[["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT"]].fillna("")
df[["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT"]] = df[["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT"]].astype(str)
df["property_street_address"] = df[["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT"]].agg(" ".join, axis=1)
df = df.drop(["STR_NUM", "STR_PFX", "Str", "STR_SFX", "STR_UNIT", "ACT"], axis=1)

df["building_year_built"] = df["building_year_built"].replace("0", pd.NA)


df["property_street_address"] = df["property_street_address"].replace(" nan ", " ")
df["property_street_address"] = df["property_street_address"].str.strip()
df["property_street_address"] = df["property_street_address"].progress_apply(lambda x: " ".join(x.split()))

df["sale_datetime"] = df["sale_datetime"].progress_apply(lambda x: date_parse(x))

df["property_zip5"] = df["property_zip5"].progress_apply(lambda x: str(x)[:5] if x != "nan" else pd.NA)
df["property_zip5"] = df["property_zip5"].progress_apply(lambda x: x if x != "nan" else pd.NA)


df.to_csv("extracted_data.csv", na_rep="", index=False)
