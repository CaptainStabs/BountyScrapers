import csv
from tqdm import tqdm
from dateutil import parser
# ,,,,,,
#SourceParcel,,mtransferDate,FromDeededOwner,,ToDeededOwner,msalesAmount,mlocCity,mlocState,mlocZipCode,mnumOfProperties,YearBuilt,
columns = ["property_id", "sale_date", "seller_name", "buyer_name", "physical_address", "sale_price", "city", "zip5", "num_units", "year_built", "county", "state", "source_url"]
with open("GovernmaxTransferHistoryExtract.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["SourceParcel"]).strip(),
                    "sale_date": str(parser.parse(row["mtransferDate"])),
                    "seller_name": " ".join(str(row["FromDeededOwner"]).split()),
                    "buyer_name": " ".join(str(row["ToDeededOwner"]).split()),
                    "sale_price": row["msalesAmount"],
                    "city": str(row["mlocCity"]).upper().strip(),
                    "zip5": row["mlocZipCode"],
                    "state": str(row["mlocState"]).strip(),
                    "county": "MEDINA",
                    "source_url": "https://www.medinacountyauditor.org/MedinaGovernmaxTransfer.zip"

                }

                # If address is in separate fields
                street_list = [str(row["mlocStrNo"]).strip(), str(row["mlocStrDir"]).strip(), str(row["mlocStrName"]).strip(), str(row["mlocStrSuffix"]).strip(), str(row["mlocStrSuffixDir"]).strip(), str(row["msecondaryAddress"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()


                # Delete if no year_built
                try:
                    if int(row["YearBuilt"]) != 0 and int(row["YearBuilt"]) <= 2022:
                        land_info["year_built"] = row["YearBuilt"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["mnumOfProperties"]) != 0:
                        land_info["num_units"] = row["mnumOfProperties"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022 and land_info["state"] != "":
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
