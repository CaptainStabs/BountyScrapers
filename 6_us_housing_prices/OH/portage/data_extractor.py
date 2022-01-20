import csv
from dateutil import parser
import re
from tqdm import tqdm


columns = ["property_id", "physical_address", "city", "county", "state", "zip5", "book", "page", "sale_date", "sale_price", "num_units", "source_url", "buyer_name"]
with open("GovernmaxExtract.txt", "r") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1
    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv, delimiter="|")

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "state": "OH",
                "county": "Portage",
                "property_id": row["mpropertyNumber"].strip(),
                "city": row["mlocCity"].strip(),
                "zip5": re.match('[0-9]{5}', row["mlocZipCode"]),
                "sale_price": row["SaleAmount"].strip(),
                "source_url": "https://www.portagecounty-oh.gov/geographic-information-systems/pages/data-downloads",
                "buyer_name": " ".join(str(row["DeededOwner"]).strip().split())
            }
            # Add street parts to list
            street_list = [str(row["mlocStrDir"]).strip(), str(row["mlocStrNo"]).strip(), str(row["mlocStrNo2"]).strip(), str(row["mlocStrName"]).strip(), str(row["mlocStrSuffix"]).strip(), str(row["mlocStrSuffixDir"]).strip()]

            # concat the street parts filtering out blank parts
            land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

            if land_info["zip5"] == "0" or land_info["zip5"] == "00000":
                land_info["zip5"] = ""

            if row["mdeedVolume"] and row["mdeedPage"]:
                try:
                    if int(row["mdeedVolume"]) > 0:
                        land_info["book"] = str(row["mdeedVolume"]).strip()

                    if int(row["mdeedPage"]) > 0:
                        land_info["page"] =  str(row["mdeedPage"]).strip()

                except:
                    continue
            try:
                land_info["sale_date"] = parser.parse(row["SaleDate"].strip())

            except:
                continue

            try:
                if int(row["NumberOfPropertiesInSale"]) > 0:
                    land_info["num_units"] = int(row["NumberOfPropertiesInSale"])

            except:
                continue

            if land_info["physical_address"] and land_info["state"] and land_info["sale_date"]:
                writer.writerow(land_info)
