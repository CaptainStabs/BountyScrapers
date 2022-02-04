import csv
from tqdm import tqdm
from dateutil import parser

# ''GPN', ' 'SitusAddress', 'SitusCity', 'SitusZip','ClassValue',  'TaxYear0BillNumber5', 'TaxYear0LevyRate5', 'TaxYear0Install1Due', 'TaxYear0Install1Paid', 'TaxYear0Install1Balance', 'TaxYear0Install1DateDue', 'TaxYear0Install1DateOverdue', 'TaxYear0Install1DatePaid', 'TaxYear0Install1Delinquent', 'TaxYear0Install2Due', 'TaxYear0Install2Paid', 'TaxYear0Install2Balance', 'TaxYear0Install2DateDue', 'TaxYear0Install2DateOverdue', 'TaxYear0Install2DatePaid', 'TaxYear0Install2Delinquent', 'TaxYear0BillNumberSA1', 'TaxYear0BillNumberSA2', 'TaxYear0BillNumberSA3', 'TaxYear0BillNumberSA4', 'TaxYear0BillNumberSA5', 'TaxYear0BillNumberSA6', 'TaxYear0BillNumberSA7', 'TaxYear0BillNumberSA8', 'TaxYear0BillNumberSA9', 'TaxYear0BillNumberSA10', 'TaxYear0SADue', 'TaxYear0SAPaid', 'TaxYear0SABalance', 'TaxYear0SADateDue', 'TaxYear0SADateOverdue', 'TaxYear0SADatePaid', 'TaxYear0SADelinquent', 'TaxYear1', 'TaxYear1TaxGross', 'TaxYear1TaxNet', 'TaxYear1TaxCredit', 'TaxYear1BillNumber1', 'TaxYear1LevyRate1', 'TaxYear1BillNumber2', 'TaxYear1LevyRate2', 'TaxYear1BillNumber3', 'TaxYear1LevyRate3', 'TaxYear1BillNumber4', 'TaxYear1LevyRate4', 'TaxYear1BillNumber5', 'TaxYear1LevyRate5', 'TaxYear1Install1Due', 'TaxYear1Install1Paid', 'TaxYear1Install1Balance', 'TaxYear1Install1DateDue', 'TaxYear1Install1DateOverdue', 'TaxYear1Install1DatePaid', 'TaxYear1Install1Delinquent', 'TaxYear1Install2Due', 'TaxYear1Install2Paid', 'TaxYear1Install2Balance', 'TaxYear1Install2DateDue', 'TaxYear1Install2DateOverdue', 'TaxYear1Install2DatePaid', 'TaxYear1Install2Delinquent', 'TaxYear1BillNumberSA1', 'TaxYear1BillNumberSA2', 'TaxYear1BillNumberSA3', 'TaxYear1BillNumberSA4', 'TaxYear1BillNumberSA5', 'TaxYear1BillNumberSA6', 'TaxYear1BillNumberSA7', 'TaxYear1BillNumberSA8', 'TaxYear1BillNumberSA9', 'TaxYear1BillNumberSA10', 'TaxYear1SADue', 'TaxYear1SAPaid', 'TaxYear1SABalance', 'TaxYear1SADateDue', 'TaxYear1SADateOverdue', 'TaxYear1SADatePaid', 'TaxYear1SADelinquent', 'TaxYear2', 'TaxYear2TaxGross', 'TaxYear2TaxNet', 'TaxYear2TaxCredit', 'TaxYear2BillNumber1', 'TaxYear2LevyRate1', 'TaxYear2BillNumber2', 'TaxYear2LevyRate2', 'TaxYear2BillNumber3', 'TaxYear2LevyRate3', 'TaxYear2BillNumber4', 'TaxYear2LevyRate4', 'TaxYear2BillNumber5', 'TaxYear2LevyRate5', 'TaxYear2Install1Due', 'TaxYear2Install1Paid', 'TaxYear2Install1Balance', 'TaxYear2Install1DateDue', 'TaxYear2Install1DateOverdue', 'TaxYear2Install1DatePaid', 'TaxYear2Install1Delinquent', 'TaxYear2Install2Due', 'TaxYear2Install2Paid', 'TaxYear2Install2Balance', 'TaxYear2Install2DateDue', 'TaxYear2Install2DateOverdue', 'TaxYear2Install2DatePaid', 'TaxYear2Install2Delinquent', 'TaxYear2BillNumberSA1', 'TaxYear2BillNumberSA2', 'TaxYear2BillNumberSA3', 'TaxYear2BillNumberSA4', 'TaxYear2BillNumberSA5', 'TaxYear2BillNumberSA6', 'TaxYear2BillNumberSA7', 'TaxYear2BillNumberSA8', 'TaxYear2BillNumberSA9', 'TaxYear2BillNumberSA10', 'TaxYear2SADue', 'TaxYear2SAPaid', 'TaxYear2SABalance', 'TaxYear2SADateDue', 'TaxYear2SADateOverdue', 'TaxYear2SADatePaid', 'TaxYear2SADelinquent', 'TaxSale1Certificate', 'TaxSale1DateSale', 'TaxSale1DateRedemption', 'TaxSale1BuyerAmount', 'TaxSale2Certificate', 'TaxSale2DateSale', 'TaxSale2DateRedemption', 'TaxSale2BuyerAmount', 'TaxSale3Certificate', 'TaxSale3DateSale', 'TaxSale3DateRedemption', 'TaxSale3BuyerAmount', 'TaxSale4Certificate', 'TaxSale4DateSale', 'TaxSale4DateRedemption', 'TaxSale4BuyerAmount', 'TaxSale5Certificate', 'TaxSale5DateSale', 'TaxSale5DateRedemption', 'TaxSale5BuyerAmount', 'CreditTotalValue', 'PropertyPhotoDate', 'PropertyPhotoLink', 'AssessorLink', 'RecorderLink', 'PropertyReportLink', 'TaxSystemDate', 'ModifiedDate', 'SHAPE', 'SHAPE.STArea()', 'SHAPE.STLength()'
columns = ["property_id", "physical_address", "sale_date", "sale_price", "property_type", "seller_name", "year_built", "county", "state", "source_url"]
with open("Parcels_Proval_010622.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "physical_address": " ".join(str(row["PropertySt"]).upper().split()),
                    "property_type": " ".join(str(row["CondDesc"]).split()),
                    "county": "Union",
                    "state": "NC",
                    "source_url": "https://www.unioncountync.gov/government/departments-f-p/gis-mapping/downloadable-gis-data"
                }

                # Delete if no year_built
                try:
                    if int(row["YrBuilt"]) != 0 and int(row["YrBuilt"]) <= 2022:
                        land_info["year_built"] = row["YrBuilt"]

                except ValueError:
                    pass

                for i in range(1,4):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_date"] = str(parser.parse(row[f"Sale{i}D"]))
                        land_info["sale_price"] = row[f"Sale{i}Amt"]
                        land_info["seller_name"] = row[f"GrantorN{i}"]
                    except parser._parser.ParserError:
                        continue

                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
