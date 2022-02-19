import csv
from dateutil import parser

# Parcel Id,Street#,Direction,Street Name,Abbrev,Book,Page,Sale Date ,Sale Amt

columns = ["property_id", "physical_address", "book", "page", "sale_date", "sale_price", "state", "county", "source_url"]

with open("Property_Sales_List.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            land_info = {
                "property_id": "".join(str(row["Parcel Id"]).strip().split()),
                "sale_date": str(parser.parse(row["Sale Date "])),
                "sale_price": row["Sale Amt"],
                "source_url": "http://gis.cravencountync.gov/downloads-zip-files.aspx",
                "state": "NC",
                "county": "Craven"
            }


            street_list = [str(row["Street#"]).strip(), str(row["Direction"]).strip(), str(row["Street Name"]).strip(), str(row["Abbrev"]).strip()]

            # concat the street parts filtering out blank parts
            land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

            if int(row["Book"]) != 0 and int(row["Page"]) != 0:
                land_info["book"] = str(row["Book"]).strip()
                land_info["page"] = str(row["Page"]).strip()

            if land_info["physical_address"] and land_info["sale_date"]:
                writer.writerow(land_info)
