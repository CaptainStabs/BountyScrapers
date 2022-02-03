import csv
from tqdm import tqdm
from dateutil import parser
#,PIN,,,,year_built,improve_eff_year_built,,sale_amt1,sale_amt2,sale_date1,sale_date2,situs_addr_city,situs_addr_line_1,situs_addr_line_2,,situs_addr_state_legdat,situs_addr_zip_legdat,,,,,,,, ,oby_yrblt1,style_desc

# sale_amt1,sale_amt2,sale_date1,sale_date2,
# year_built,improve_eff_year_built,,
# situs_addr_city,situs_addr_line_1,situs_addr_line_2,,situs_addr_state_legdat,situs_addr_zip_legdat
#,PIN,,,,,,,,,,,, ,oby_yrblt1,style_desc
#                d            d                 d        d           d          d                   d           d      d                   
columns = ["property_id", "year_built", "sale_price", "sale_date", "city", "physical_address", "num_units", "zip5", "property_type", "county", "state", "source_url"]
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
                    "property_id": row["PIN"],
                    "city": " ".join(str(row["situs_addr_city"]).upper().split()),
                    "property_type": " ".join(str(row["style_desc"]).upper().split()),
                    "zip5": row["situs_addr_zip_legdat"],
                    "county": "LAKE",
                    "state": "IL",
                    "source_url": "https://www.unioncountync.gov/government/departments-f-p/gis-mapping/downloadable-gis-data"
                }


                # If address is in separate fields
                street_list = [str(row["situs_addr_line_1"]).strip(), str(row["situs_addr_line_2"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                if not row["year_built"] and row["improve_eff_year_built"]:
                    # Delete if no year_built
                    try:
                        if int(row["improve_eff_year_built"]) != 0 and int(row["improve_eff_year_built"]) <= 2022:
                            land_info["year_built"] = row["improve_eff_year_built"]

                    except ValueError:
                        pass

                if row["year_built"] and not row["improve_eff_year_built"]:
                    # Delete if no year_built
                    try:
                        if int(row["year_built"]) != 0 and int(row["year_built"]) <= 2022:
                            land_info["year_built"] = row["year_built"]

                    except ValueError:
                        pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["multi_bldg"]) != 0:
                        land_info["num_units"] = row["multi_bldg"]
                except ValueError:
                    pass

                for i in range(1,3):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_date"] = str(parser.parse(row[f"sale_date{i}"]))
                        land_info["sale_price"] = row[f"sale_amt{i}"]

                    except parser._parser.ParserError:
                        continue

                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
