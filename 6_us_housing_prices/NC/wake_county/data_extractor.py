import csv
from dateutil import parser
from tqdm import tqdm

columns = ["physical_address", "sale_date", ]
with open("test.csv", "r", newline="") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    csv_reader = csv.DictReader(input_csv)

    with open("wake_county.csv", "a", newline="") as output_csv:
        writer=  csv.DictWriter(output_csv, fieldnames=columns)

        for row in tqdm(csv_reader, total=line_count):
            land_info = {}
            #
            # # Add street parts to list
            # street_list = [str(row["Street_Number"]).strip(), str(row["Street_Prefix"]).strip(), str(row["Street_Name"]).strip(), str(row["Street_Type"]).strip(), str(row["Street_Suffix"]).strip(), str(row["Street_Misc"]).strip()]
            #
            # # concat the street parts filtering out blank parts
            # land_info["physical_address"] = ' '.join(filter(None, street_list))


            if row["Land_Sale_Date"] and row["Total_Sale_Date"]:
                # land_info["sale_date"] = parser.parse(str(row["Total_Sale_Date"]))
                print("Both")

            elif row["Land_Sale_Date"] and not row["Total_Sale_Date"]:
                # land_info['sale_date'] = parser.parse(str(row["Land_Sale_Date"]))
                print("Land_Sale_Date")

            elif row["Total_Sale_Date"] and not row["Land_Sale_Date"]:
                land_info['sale_date'] = parser.parse(str(row["Total_Sale_Date"]))
                print("Total_Sale_Date")
