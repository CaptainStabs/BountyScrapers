import csv
from tqdm import tqdm
from sale_type import deed_type

import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse


# ParcelID,DeedType,Grantor,Grantee,SaleDate,SaleAmount
columns = ["property_id", "physical_address", "sale_type", "seller_name", "buyer_name", "sale_date", "sale_price", "county", "state", "source_url", "land_appraised_value", "land_assessed_value", "building_appraised_value", "building_assessed_value", "land_area_sqft", "land_area_acres", "building_area_sqft"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["ParcelID"],
                    "seller_name": " ".join(str(row["Grantor"]).upper().split()),
                    "buyer_name": " ".join(str(row["Grantee"]).upper().split()),
                    "sale_date": str(date_parse(row["SaleDate"])),
                    "sale_price": row["SaleAmount"],
                    "county": "WASHOE",
                    "state": "NV",
                    "source_url": "https://gis.washoecounty.us/webservices/gisdataservice/DocumentFiles/AssessorOnlineReports/A7BE5E322AA4WC531ADMINCF8BC6597CX2B4/?fileId=GSAQuickInfo_2021Final.zip",
                    "land_appraised_value": row["LandAppraised"],
                    "land_assessed_value": row["LandAssessed"],
                    "building_appraised_value": row["ImprovmentAppraised"],
                    "building_assessed_value": row["ImprovmentAssessed"],
                    "building_area_sqft": row["BldgSquareFeet"]

                }

                if row["LandUnitType"] == "SF":
                    land_info["land_area_sqft"] = row["LandArea"]
                elif row["LandUnitType"] == "AC":
                    land_info["land_area_acres"] = row["LandArea"]
                if row["DeedType"].strip():
                    try:
                        land_info["sale_type"] = str(deed_type[row["DeedType"]]).upper()
                    except KeyError:
                        # print(row["DeedType"])
                        land_info["sale_type"] = row["DeedType"].upper().strip()
                else:
                    try:
                        land_info["sale_type"] = str(deed_type[str(row["SaleVerificationCode"]).upper()]).upper()
                    except KeyError:
                        land_info["sale_type"] = str(row["SaleVerificationCode"]).upper()
                 # ,,,
                # If address is in separate fields
                street_list = [str(row["SitusNumber"]).strip(), str(row["SitusDirection"]).strip(), str(row["SitusStreet"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
