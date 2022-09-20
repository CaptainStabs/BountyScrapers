import pandas as pd
import numpy as np

df = pd.read_csv("sf_assessor.csv")

# OBJECTID,AssessorMulti_Project_BLOCK,AssessorMulti_Project_LOT,AssessorMulti_Project_USECODE,AssessorMulti_Project_CONSTRUCTION,AssessorMulti_Project_LOTSHAPE,AssessorMulti_Project_LOTFRONTAGE,AssessorMulti_Project_LOTDEPTH,AssessorMulti_Project_BASEMENT, ,AssessorMulti_Project_OWNER_NAME,AssessorMulti_Project_OWNER_ADDRESS,AssessorMulti_Project_OWNER_CITY,AssessorMulti_Project_OWNER_STATE,AssessorMulti_Project_OWNER_ZIP,AssessorMulti_Project_OWNER_PERCENTAGE,AssessorMulti_Project_OWNER_DATE,ConstrType_ConstrDesc,
df.rename(
    columns={
        "AssessorMulti_Project_BLKLOT": "property_id",
        "AssessorMulti_Project_ADDRESS": "property_street_address",
        "AssessorMulti_Project_CURRPRICE": "sale_price",
        "AssessorMulti_Project_CURRSALEDATE": "sale_datetime",
        "AssessorMulti_Project_LOTAREA": "land_area_sqft",
        "AssessorMulti_Project_STORIES": "building_num_stories",
        "AssessorMulti_Project_UNITS": "building_num_units",
        "AssessorMulti_Project_BEDROOMS": "building_num_beds",
        "AssessorMulti_Project_BATHROOMS": "building_num_baths",
        "AssessorMulti_Project_BLDGSQFT": "building_area_sqft",
        "AssessorMulti_Project_YRBUILT": "building_year_built",
        "UseClass_DESCRIPTION": "property_type",
    },
    inplace=True,
)

# df["sale_datetime"] = df["sale_datetime"].apply(lambda x: date_parse(x))
df["sale_datetime"] = pd.to_datetime(df["sale_datetime"], unit='ms')
df["source_url"] = df["property_id"].apply(
    lambda x: f"https://sfplanninggis.org/pim/?tab=Property&search={x}"
)
df.drop(
    [
        "OBJECTID",
        "AssessorMulti_Project_BLOCK",
        "AssessorMulti_Project_LOT",
        "AssessorMulti_Project_USECODE",
        "AssessorMulti_Project_CONSTRUCTION",
        "AssessorMulti_Project_LOTSHAPE",
        "AssessorMulti_Project_LOTFRONTAGE",
        "AssessorMulti_Project_LOTDEPTH",
        "AssessorMulti_Project_BASEMENT",
        "AssessorMulti_Project_OWNER_NAME",
        "AssessorMulti_Project_OWNER_ADDRESS",
        "AssessorMulti_Project_OWNER_CITY",
        "AssessorMulti_Project_OWNER_STATE",
        "AssessorMulti_Project_OWNER_ZIP",
        "AssessorMulti_Project_OWNER_PERCENTAGE",
        "AssessorMulti_Project_OWNER_DATE",
        "ConstrType_ConstrDesc",
        "AssessorMulti_Project_LANDVAL",
        "AssessorMulti_Project_STRUCVAL",
        "AssessorMulti_Project_FIXTVAL",
        "AssessorMulti_Project_OTHRVAL",
        "AssessorMulti_Project_PRIORPRICE",
        "AssessorMulti_Project_PRIORSALEDATE",
        "AssessorMulti_Project_ROOMS"
    ],
    axis=1,
    inplace=True,
)

df = df.dropna(subset=["property_street_address", "sale_price", "sale_datetime"], axis=0)
df["state"] = "CA"
df["property_county"] = "SAN FRANCISCO"
# df["property_city"] = "SAN FRANCISCO"
df["building_year_built"] = np.where(df["building_year_built"] > 1492, df["building_year_built"], pd.NA)
df = df.applymap(lambda x: " ".join(x.strip().strip().split()) if isinstance(x, str) else x)

# print(df.columns)
df.to_csv("extracted_data.csv", index=False)
