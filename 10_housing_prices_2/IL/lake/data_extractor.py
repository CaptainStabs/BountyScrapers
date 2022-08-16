import csv
from tqdm import tqdm
from dateutil import parser
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse

#,PIN,,,,year_built,improve_eff_year_built,,sale_amt1,sale_amt2,sale_date1,sale_date2,situs_addr_city,situs_addr_line_1,situs_addr_line_2,,situs_addr_state_legdat,situs_addr_zip_legdat,,,,,,,, ,oby_yrblt1,style_desc

# sale_amt1,sale_amt2,sale_date1,sale_date2,
# year_built,improve_eff_year_built,,
# situs_addr_city,situs_addr_line_1,situs_addr_line_2,,situs_addr_state_legdat,situs_addr_zip_legdat
#,PIN,,,,,,,,,,,, ,oby_yrblt1,style_desc
#                d            d                 d        d           d          d                   d           d      d
columns = ["property_id", "building_year_built", "sale_price", "sale_datetime", "property_city", "property_street_address", "building_num_units", "property_zip5", "property_type", "sale_type", "property_county", "state", "source_url", "land_area_acres", "building_area_sqft", "building_num_beds", "property_township", "building_num_baths", 'assessed_total', 'building_assessed_date', 'building_assessed_value', 'land_assessed_date', 'land_assessed_value', "building_num_stories"]
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
                    "property_city": " ".join(str(row["situs_addr_city"]).upper().split()),
                    "property_type": " ".join(str(row["style_desc"]).upper().split()),
                    "property_zip5": row["situs_addr_zip_legdat"],
                    "property_county": "LAKE",
                    "state": "IL",
                    "source_url": "https://www.unioncountync.gov/government/departments-f-p/gis-mapping/downloadable-gis-data",
                    "building_num_beds": row["bedroom_count"],
                    "building_assessed_value": row["assess_bldg_assyr"],
                    "land_assessed_value": row["assess_land_assyr"],
                    "assessed_total": row["assess_total_assyr"],
                    "land_assessed_date": date_parse(row["assessment_year"]),
                    "building_assessed_date": date_parse(row["assessment_year"]),
                    "property_township": row["township"],
                    "building_num_stories": row["stories"].replace(" STORY", "").strip()
                }


                cca = row["calculated_cama_acres"]
                da = row["deeded_acres"]
                if cca:
                    land_info["land_area_acres"] = cca
                elif da:
                    land_info["land_area_acres"] = da

                areasum_c = int(row["areasum_c"]) if row["areasum_c"] else 0
                spec_srvc_area = int(ow["spec_srvc_area"]) if row["spec_srvc_area"] else 0
                upper_sq_ft = int(row["upper_sq_ft"]) if row["upper_sq_ft"] else 0
                shedsqft = int(row["shedsqft"]) if row["shedsqft"] else 0
                second_sq_ft = int(row["second_sq_ft"]) if row["second_sq_ft"] else 0
                poolsqft = int(row["poolsqft"]) if row["poolsqft"] else 0
                polebldgsqft = int(row["polebldgsqft"]) if row["polebldgsqft"] else 0
                bsmt_sq_ft_fin = int(row["bsmt_sq_ft_fin"]) if row["bsmt_sq_ft_fin"] else 0
                bsmt_sq_ft = int(row["bsmt_sq_ft"]) if row["bsmt_sq_ft"] else 0
                lower_sq_ft_fin = int(row["lower_sq_ft_fin"]) if row["lower_sq_ft_fin"] else 0
                lower_sq_ft = int(row["lower_sq_ft"]) if row["lower_sq_ft"] else 0
                liv_sq_ft = int(row["liv_sq_ft"]) if row["liv_sq_ft"] else 0
                gazebosqft = int(row["gazebosqft"]) if row["gazebosqft"] else 0
                first_sq_ft = int(row["first_sq_ft"]) if row["first_sq_ft"] else 0
                attic_sq_ft = int(row["attic_sq_ft"]) if row["attic_sq_ft"] else 0
                area_sf = int(row["area_sf"]) if row["area_sf"] else 0

                sqft = sum([areasum_c, spec_srvc_area, upper_sq_ft, shedsqft, second_sq_ft, poolsqft, polebldgsqft, bsmt_sq_ft_fin, bsmt_sq_ft, lower_sq_ft_fin, lower_sq_ft, liv_sq_ft, gazebosqft, first_sq_ft, attic_sq_ft, area_sf])

                if sqft:
                    land_info["building_area_sqft"] = sqft
                # If address is in separate fields
                street_list = [str(row["situs_addr_line_1"]).strip(), str(row["situs_addr_line_2"]).strip()]

                full_baths = int(row["full_baths"]) if row["full_baths"] else 0
                half_baths = int(row["half_baths"]) if row["half_baths"] else 0
                baths = sum([full_baths, half_baths * 0.5])



                # concat the street parts filtering out blank parts
                land_info["property_street_address"] = ' '.join(filter(None, street_list)).upper()

                if not row["year_built"] and row["improve_eff_year_built"]:
                    # Delete if no year_built
                    try:
                        if int(row["improve_eff_year_built"]) != 0 and int(row["improve_eff_year_built"]) <= 2022:
                            land_info["building_year_built"] = row["improve_eff_year_built"]

                    except ValueError:
                        pass

                if row["year_built"] and not row["improve_eff_year_built"]:
                    # Delete if no year_built
                    try:
                        if int(row["year_built"]) != 0 and int(row["year_built"]) <= 2022:
                            land_info["building_year_built"] = row["year_built"]

                    except ValueError:
                        pass

                # Delete if no zip5
                if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                    land_info["property_zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["multi_bldg"]) != 0:
                        land_info["building_num_units"] = row["multi_bldg"]
                except ValueError:
                    pass

                for i in range(1,3):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_datetime"] = str(date_parse(row[f"sale_date{i}"]))
                        land_info["sale_price"] = row[f"sale_amt{i}"]
                        land_info["sale_type"] = str(row[f"deed_type{i}"]).upper().strip()
                        year = land_info["sale_datetime"].split("-")[0]

                        if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)

                    except parser._parser.ParserError:
                        pass



            except parser._parser.ParserError:
                pass
