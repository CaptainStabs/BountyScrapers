import csv
from tqdm import tqdm
from dateutil import parser

# ParcelID,TransferBook,TransferPage,PlatBook,PlatPage,DateSold,SalePrice,PropertyAddress,Complex,LandUse,LandUseDesc,ImprovedStatus,BldgTypeDesc,,BuildingCount,Own

columns = ["property_id", "book", "page", "sale_date", "sale_price", "physical_address", "property_type", "num_units", "source_url", "state", "SC"]

with open("Parcels.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_dated.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            try:
                # print(row)
                # break
                land_info = {
                    "property_id": row["ParcelID"],
                    "book": row["TransferBook"],
                    "page": row["TransferPage"],
                    "sale_date": parser.parse(str(row["DateSold"]).replace("+00", "")),
                    "sale_price": row["SalePrice"],
                    "physical_address": " ".join(str(row["PropertyAddress"]).upper().strip().split()),
                    "property_type": row["SaleLandUse"],
                    "source_url": "https://opendata-yorkcosc.hub.arcgis.com/datasets/parcels-york-county-sc/explore"
                }

                if row["BuildingCount"]:
                    land_info["num_units"] = row["BuildingCount"]

                if land_info["physical_address"] and land_info["sale_date"]:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                # print(row["DateSold"])
                continue
