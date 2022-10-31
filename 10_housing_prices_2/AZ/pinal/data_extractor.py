import csv
from tqdm import tqdm
from dateutil import parser
import usaddress
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse


# ,CLASSCD,CLASSDSCRP,SITEADDRESS,FLOORCOUNT,,,STRCLASS,CLASSMOD,LNDVALUE,PRVASSDVAL,CNTASSDVAL,ASSDVALYRCG,ASSDPCNTCG,PRVTXBLVAL,CNTTXBLVAL,TXBLVALYRCHG,TXBLPCNTCHG,PRVWNTTXOD,PRVSMRTXOD,TOTPRVTXTOD,CNTWNTTXOD,CNTSMRTXOD,TOTCNTTXOD,TXODYRCHG,TXODPCNTCHG,LASTUPDATE,SALEDATE,SALEPRICE,DEFAULTAPPROACH,EA,GROSSSF,GROSSAC,DEFAULTLEA,VALUEMEASURE,VALUEPER,LEA,ADJUSTMENT,ATTRIBUTE,REASONTOEXCLUDE,LANDSF,OVERRIDE,RECEPTIONNO,GlobalID
columns = ["property_street_address", "property_city", "property_zip5", "building_year_built", "property_id", "property_type", "sale_datetime", "sale_price", "property_county", "state", "source_url", "building_num_stories", "building_area_sqft", "land_area_acres", "land_area_sqft"]
with open("pinal.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "sale_datetime": str(date_parse(row["SALEDATE"])),
                    "sale_price": row["SALEPRICE"],
                    "property_type": " ".join(str(row["RESSTRTYP"]).upper().split()),
                    "property_id": row["PARCELID"],
                    "property_county": "PINAL",
                    "state": "AZ",
                    "source_url": f"https://www.pinalcountyaz.gov/Assessor/Pages/ParcelSearch.aspx?parcelnumber={row['PARCELID']}",
                    "building_num_stories": row["FLOORCOUNT"],
                    "building_area_sqft": row["BLDGAREA"],
                    "land_area_sqft": row["GROSSSF"],
                    "land_area_acres": row["GROSSAC"],

                }

                property_street_address = " ".join(str(row["SITEADDRESS"]).upper().split())
                try:
                    parsed_address = usaddress.tag(property_street_address)
                    parse_success = True

                except usaddress.RepeatedLabelError as e:
                    print(e)
                    parse_success = False

                if parse_success:
                    try:
                        street_physical = str(property_street_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip()
                        street_physical = street_physical.strip(",")
                        land_info["property_street_address"] = street_physical.replace('"', '').strip(",")

                        try:
                            land_info["property_city"] = parsed_address[0]["PlaceName"]
                        except KeyError:
                            raise

                        try:
                            land_info["property_zip5"] = str(parsed_address[0]["ZipCode"]).replace('"', '').strip()
                            # Delete if no property_zip5
                            if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                                land_info["property_zip5"] = ""
                        except KeyError:
                            raise
                    except KeyError:
                        pass
                        # print("\n" + str(property_street_address))

                    # Delete if no building_year_built
                    try:
                        if int(row["RESYRBLT"]) >= 1690 and int(row["RESYRBLT"]) <= 2022:
                            land_info["building_year_built"] = row["RESYRBLT"]

                    except ValueError:
                        pass


                    try:
                        year = land_info["sale_datetime"].split("-")[0]
                        month = land_info["sale_datetime"].split("-")[1]
                        if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) < 2022:
                            writer.writerow(land_info)
                        elif int(year) == 2022 and int(month) <= 9:
                            writer.writerow(land_info)
                    except KeyError:
                        pass

            except parser._parser.ParserError:
                pass
