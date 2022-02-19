import csv
from tqdm import tqdm
from dateutil import parser

# ParcelID,TransferBook,TransferPage,PlatBook,PlatPage,DateSold,SalePrice,PropertyAddress,Complex,LandUse,LandUseDesc,ImprovedStatus,BldgTypeDesc,,BuildingCount,Own

columns = ["property_id", "book", "page", "sale_date", "sale_price", "physical_address", "property_type", "num_units", "source_url", "state"]

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
                    "property_id": row["ParcelID"].strip(),
                    "book": "".join(filter(str.isdigit, row["TransferBook"].strip().replace("O", "0"))),
                    "page": "".join(filter(str.isdigit, str(row["TransferPage"].replace("`", "").strip().replace("O", "0")))),
                    "sale_date": parser.parse(str(row["DateSold"]).replace("+00", "")),
                    "sale_price": row["SalePrice"],
                    "physical_address": " ".join(str(row["PropertyAddress"]).upper().strip().split()).strip(),
                    "property_type": row["BldgTypeDesc"].strip(),
                    "source_url": "https://opendata-yorkcosc.hub.arcgis.com/datasets/parcels-york-county-sc/explore",
                    "state": "SC"
                }

                if row["BuildingCount"]:
                    land_info["num_units"] = row["BuildingCount"]

                if land_info["book"]:
                    if not int(land_info["book"]):
                        land_info["book"] = ""

                if land_info["page"]:
                    if not int(land_info["page"]):
                        land_info["page"] = ""

                sale_date = str(land_info["sale_date"])
                year = sale_date.split("-")[0]

                if int(year) == 2022:
                    if int(sale_date.split("-")[1]) > 1:
                        save = False
                    else:
                        save = True
                        print(sale_date.split("-")[1])
                else:
                    save = True

                if save:
                    try:
                        if land_info["physical_address"] and land_info["sale_date"] and int(land_info["sale_price"]) >= 0:
                            writer.writerow(land_info)
                    except:
                        continue

            except parser._parser.ParserError:
                # print(row["DateSold"])
                continue
