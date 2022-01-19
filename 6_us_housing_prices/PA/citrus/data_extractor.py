import csv
from tqdm import tqdm
from dateutil import parser

#,LASTSALEDT,LASTSALEPRICE,,,RES_YRBUILT,COMM_YRBUILT,SITE_ZIP

columns ["property_id", "num_units", "physical_address", "sale_date", "sale_price", "book", "page", "year_built", "zip5", "state", "county", "source_url"]

with open("VD_PARCELDATA.dat", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    for row in reader:
        land_info = {
            "state": "PA",
            "county": "Citrus",
            "source_url": "https://www.citruspa.org/_dnn/Downloads",
            "property_id": row["PARCELID"],
            "city": row["SITE_ADRCITY"],
            "book": row["BOOK"],
            "page": row["PAGE"]
        }

        if row["NUMBLDG"]:
            land_info["num_units"] = row["NUMBLDG"]

        street_list = [str(row["SITE_ADRNO"]).strip(), str(row["SITE_ADRDIR"]).strip(), str(row["SITE_ADRSTR"]).strip(), str(row["SITE_ADRSUF"]).strip(), str(row["SITE_ADRSUF2"]).strip(), str(row["Street_Misc"]).strip(), str(row["SITE_UNITNO"]).strip()]

        # concat the street parts filtering out blank parts
        land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()
