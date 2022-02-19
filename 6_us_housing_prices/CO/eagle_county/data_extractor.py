import csv
from tqdm import tqdm
import os
from dateutil import parser

# S,Grantee 1,Grantor 1,Public Remark 1,Sale Date 2,Sale Price 2,Document Number 2,Doc Fee 2,Grantee 2,Grantor 2,Public Remark 2,Sale Date 3,Sale Price 3,Document Number 3,Doc Fee 3,Grantee 3,Grantor 3,Public Remark 3,Sale Date 4,Sale Price 4,Document Number 4,Doc Fee 4,Grantee 4,Grantor 4,Public Remark 4,Sale Date 5,Sale Price 5,Document Number 5,Doc Fee 5,Grantee 5,Grantor 5,Public Remark 5,Sale Date 6,Sale Price 6,Document Number 6,Doc Fee 6,Grantee 6,Grantor 6,Public Remark 6,Sale Date 7,Sale Price 7,Document Number 7,Doc Fee 7,Grantee 7,Grantor 7,Public Remark 7,Sale Date 8,Sale Price 8,Document Number 8,Doc Fee 8,Grantee 8,Grantor 8,Public Remark 8,Sale Date 9,Sale Price 9,Document Number 9,Doc Fee 9,Grantee 9,Grantor 9,Public Remark
filename = "extracted_data.csv"

columns = ["state", "physical_address", "city", "county", "property_id", "sale_date", "property_type", "sale_price", "seller_name", "buyer_name", "num_units", "year_built", "source_url",]
with open("AccountPublicExtractForWeb.csv", "r") as input_csv:
    csv_file = csv.DictReader(input_csv)

    with open(filename, "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for row in tqdm(csv_file):
            land_info = {
                "state":"CO",
                "county": "EAGLE COUNTY",
                "property_type": str(row["Building Type"]),
                "city": ' '.join(str(row["Location City"]).upper().strip().split())
            }

            street_list = [str(row["Street Number"]).strip(), str(row["Street Alpha"]).strip(), str(row["Street Direction"]).strip(), str(row["Street Name"]).strip(), str(row["Street Suffix"]).strip(), str(row["Building Number"]).strip()]

            # concat the street parts filtering out blank parts
            land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())


            res_count = row["Residential Building Count"]
            com_count = row["Commercial Building Count"]

            if res_count == "" and com_count != "":
                num_units = int(row["Commercial Building Count"])

            elif res_count != "" and com_count == "":
                num_units = int(row["Residential Building Count"])

            if res_count != "" and com_count != "":
                num_units = int(row["Residential Building Count"]) + int(row["Commercial Building Count"])


            if num_units:
                land_info["num_units"] = num_units

            if row["First Residential Year Built"] != 0:
                land_info["year_built"] = row["First Residential Year Built"]

            if not row["Parcel Number"]:
                land_info["property_id"] = row["Account Number"]

            else:
                land_info["property_id"] = row["Parcel Number"]

            land_info["source_url"] = "https://www.eaglecounty.us/assessor/propertyrecordsearch"
            for i in range(1, 10):
                if row[f"Sale Date {i}"]:
                    try:
                        land_info["sale_date"] = parser.parse(row[f"Sale Date {i}"])
                        land_info["sale_price"] = row[f"Sale Price {i}"]
                        land_info["seller_name"] = " ".join(str(row[f"Grantee {i}"]).strip().split())
                        land_info["buyer_name"] = " ".join(str(row[f"Grantor {i}"]).strip().split())
                        if land_info["physical_address"] and land_info["sale_date"]:
                            writer.writerow(land_info)
                    except parser._parser.ParserError:
                        # print(row[f"Sale Date {i}"])
                        pass
