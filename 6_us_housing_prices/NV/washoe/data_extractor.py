import csv
from tqdm import tqdm
from dateutil import parser
from sale_type import deed_type

# ParcelID,DeedType,Grantor,Grantee,SaleDate,SaleAmount
columns = ["property_id", "physical_address", "sale_type", "seller_name", "buyer_name", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\NV\\washoe\\extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["ParcelID"],
                    "seller_name": " ".join(str(row["Grantor"]).upper().split()),
                    "buyer_name": " ".join(str(row["Grantee"]).upper().split()),
                    "sale_date": str(parser.parse(row["SaleDate"])),
                    "sale_price": row["SaleAmount"],
                    "county": "WASHOE",
                    "state": "NV",
                    "source_url": "https://gis.washoecounty.us/webservices/gisdataservice/DocumentFiles/AssessorOnlineReports/A7BE5E322AA4WC531ADMINCF8BC6597CX2B4/?fileId=GSAQuickInfo_2021Final.zip",
                }

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
