import csv
from tqdm import tqdm
from dateutil import parser

#PIN,,DeedBook,DeedPage,DeedDate,SaleMonth,SaleYear,SalePrice,BuildingCo,ParcelType,ParCity,ParZipCode,ParAddress,StreetSuff,StreetType,StreetName,StreetDire,UnitNumber,HouseNumbe,
columns = ["property_id", "book", "page", "sale_date", "sale_price", "num_units", "property_type", "city", "zip5", "physical_address", "county", "state", "source_url"]
with open("TaxParcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PIN"]).split(".")[0],
                    "sale_date": str(parser.parse((str(row["SaleMonth"]) + "/01/" + str(row["SaleYear"])))),
                    "sale_price": row["SalePrice"],
                    "property_type": " ".join(str(row["ParcelType"]).upper().strip().split()),
                    "city": str(row["ParCity"]).upper(),
                    "zip5": row["ParZipCode"],
                    "county": "Harnett",
                    "state": "NC",
                    "source_url": "https://gis.harnett.org/DataDownloads/Shapefile/TaxParcels.zip"
                }


                # If address is in separate fields
                street_list = [ str(row["HouseNumbe"]).strip(), str(row["StreetDire"]).strip(), str(row["StreetName"]).strip(), str(row["StreetType"]).strip(), str(row["StreetSuff"]).strip()]

                if row["UnitNumber"]:
                    street_list.append("UNIT " + str(row["UnitNumber"]))
                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                try:
                    if int(row["BuildingCo"]) != 0:
                        land_info["num_units"] = row["BuildingCo"]

                except ValueError:
                    continue


                book = row["DeedBook"]
                page = row["DeedPage"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    continue

                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                continue
