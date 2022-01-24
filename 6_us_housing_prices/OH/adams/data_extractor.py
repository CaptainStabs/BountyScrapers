import csv
from dateutil import parser

columns = ["property_id", "physical_address", "city", "state", "zip5", "sale_date", "sale_price", "num_units", "source_url", "county"]
with open("GovernmaxExtract.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:

            land_info = {
                "property_id": row["mcamaId"],
                "city": row["mlocCity"],
                "state": row["mlocState"],
                "zip5": row["mlocZipCode"],
                "sale_price": row["SaleAmount"],
                "source_url": "https://adamscountyauditor.org/",
                "county": "Adams"

            }

            street_list = [str(row["mlocStrDir"]).strip(), str(row["mlocStrNo"]).strip(), str(row["mlocStrName"]).strip(), str(row["mlocStrSuffix"]).strip(), str(row["mlocStrSuffixDir"]).strip()]

            # concat the street parts filtering out blank parts
            land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())

            if row["NumberOfPropertiesInSale"]:
                land_info["num_units"] = row["NumberOfPropertiesInSale"]

            try:
                land_info["sale_date"] = parser.parse(row["SaleDate"])

            except:
                pass

            try:
                if land_info["num_units"] == 0:
                    land_info["num_units"] = ""
            except KeyError:
                pass


            try:
                if land_info["sale_date"] and land_info["state"] and land_info["physical_address"]:
                    writer.writerow(land_info)
            except Exception as e:
                print(e)
