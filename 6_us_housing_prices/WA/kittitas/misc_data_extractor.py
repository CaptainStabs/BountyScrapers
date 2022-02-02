import csv
from tqdm import tqdm
from dateutil import parser

# "ParcelNumber","SaleDate","OriginalSalePrice","Grantor","Grantee","DepartmentOfRevenueCode","Situs","DORCode","MiscImp","NumberOfUnits"
columns = ["property_id", "sale_date", "sale_price", "seller_name", "buyer_name", "property_type", "physical_address", "num_units", "county", "state", "source_url"]
with open(".\\input_data\\Misc.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open(".\\extracted_data\\misc_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                try:
                    if row["OriginalSalePrice"]:
                        land_info = {
                            "property_id": row["ParcelNumber"],
                            "sale_date": str(parser.parse(row["SaleDate"])),
                            "sale_price": row["OriginalSalePrice"].split(".")[0],
                            "seller_name": " ".join(str(row["Grantor"]).upper().split()),
                            "buyer_name": " ".join(str(row["Grantee"]).upper().split()),
                            "physical_address": " ".join(str(row["Situs"]).upper().split()),
                            "county": "KITTITAS",
                            "state": "WA",
                            "source_url": "https://data-kitcogis.opendata.arcgis.com/search?q=parcel",
                        }

                        # If address is in separate fields
                        type_list = [str(row["DORCode"]).strip(), str(row["MiscImp"]).strip()]

                        # concat the street parts filtering out blank parts
                        # land_info["property_type"] = '; '.join(filter(None, type_list)).upper()
                        land_info["property_type"] = " ".join(str('; '.join(filter(None, type_list)).upper()).split())

                        try:
                            # Delete if no unit count
                            if int(row["NumberOfUnits"].split(".")[0]) != 0:
                                land_info["num_units"] = row["NumberOfUnits"].split(".")[0]
                        except ValueError:
                            pass

                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)
                except KeyError:
                    raise KeyError
                    pass

            except parser._parser.ParserError:
                pass
