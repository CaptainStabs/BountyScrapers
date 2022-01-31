import csv
from tqdm import tqdm
from dateutil import parser
# "or_bk","or_pg","grantor","grantee","dos","price","str_num","str","str_num_sfx","str_pfx","str_sfx","str_sfx_dir","city","str_unit","zip","num","dscr","strap"
# str_num,str_num_sfx,str_pfx,str,str_sfx,str_sfx_dir,str_unit,
# or_bk,or_pg,grantor,grantee,price,dos,zip,city,strap,dscr
columns = ["book", "page", "seller_name", "buyer_name", "sale_price", "sale_date", "physical_address", "zip5", "city", "property_id", "num_units", "property_type", "county", "state", "source_url"]
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
                    "seller_name": " ".join(str(row["grantor"]).upper().split()),
                    "buyer_name": " ".join(str(row["grantee"]).upper().split()),
                    "sale_price": str(row["price"]).strip(),
                    "sale_date": str(parser.parse(row["dos"])),
                    "zip5": str(row["zip"]).strip(),
                    "city": " ".join(str(row["city"]).upper().split()),
                    "property_id": str(row["strap"]).strip(),
                    "property_type": " ".join(str(row["dscr"]).upper().split()),
                    "county": "ST. JOHNS",
                    "state": "FL",
                    "source_url": "https://www.sjcpa.us/formsdata/"

                }

                # If address is in separate fields
                # ,,,,,,
                street_list = [str(row["str_num"]).strip(), str(row["str_num_sfx"]).strip(), str(row["str_pfx"]).strip(), str(row["str"]).strip(), str(row["str_sfx"]).strip(), str(row["str_sfx_dir"]).strip(), str(row["str_unit"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["or_bk"]).strip()
                page = str(row["or_pg"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                try:
                    # Delete if no zip5
                    if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                        land_info["zip5"] = ""
                except KeyError:
                    pass

                try:
                    # Delete if no unit count
                    if int(row["num"]) != 0:
                        land_info["num_units"] = int(row["num"])
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
