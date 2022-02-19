import csv
from tqdm import tqdm
from dateutil import parser

# PIN,mlocAddr,mlocCity,mlocState,mlocZipCod,,SaleDate,,SaleAmount,

columns = ["property_id", "physical_address", "city", "state", "zip5", "sale_date", "sale_price", "source_url", "county"]

with open("WayneCoOH_Parcels_Attributed.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "physical_address": " ".join(str(row["mlocAddr"]).upper().strip().split()),
                    "city": str(row["mlocCity"]).strip(),
                    "state": str(row["mlocState"]).strip(),
                    "zip5": str(row["mlocZipCod"]).strip(),
                    "sale_date": str(parser.parse(row["SaleDate"])).replace("+00:00", ""),
                    "sale_price": row["SaleAmount"],
                    "source_url": "https://data-waynecountygis.opendata.arcgis.com/datasets/7653be749b4d4e5289331becd8dbf71f_0/about",
                    "county": "Wayne"
                }

                if "-" in land_info["zip5"]:
                    print(land_info["zip5"])

                if not land_info["state"] or land_info["state"] == " ":
                    land_info["state"] = "OH"

                if land_info["physical_address"] and land_info["state"] and land_info["sale_date"] and int(land_info["sale_price"]) >= 0:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                # print(row["SaleDate"])
                pass
