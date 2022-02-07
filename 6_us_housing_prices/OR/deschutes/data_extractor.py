import csv
from tqdm import tqdm
from dateutil import parser

# "Taxlot","Book_Page_1","Total_Sales_Price_1","Sales_Date_1","Seller_1","Buyer_1","Book_Page_2","Total_Sales_Price_2","Sales_Date_2","Seller_2","Buyer_2","Address","Expr1012","Unit_Number","City","State","Zip","Year_Built_1","Year_Built_2"

# "Book_Page_1","Total_Sales_Price_1","Sales_Date_1","Seller_1","Buyer_1","Book_Page_2","Total_Sales_Price_2","Sales_Date_2","Seller_2","Buyer_2",
# "Address","Unit_Number",
# "City","State","Zip","Year_Built_1","Year_Built_2"
columns = ["property_id", "physical_address", "book", "page", "sale_price", "sale_date", "seller_name", "buyer_name",  "year_built", "city", "zip5", "property_type", "county", "state", "source_url"]
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
                    "property_id": row["Taxlot"],
                    "city": " ".join(str(row["City"]).upper().split()),
                    "zip5": row["Zip"],
                    "property_type": " ".join(str(row["Stat_Class_Desc_1"]).upper().split()),
                    "county": "DESCHUTES",
                    "state": "OR",
                    "source_url": "https://data.deschutes.org/datasets/gis-sales-1/explore"
                }


                # If address is in separate fields
                if str(row["Unit_Number"]):
                    street_list = [str(row["Address"]).strip(), str("UNIT " + str(row["Unit_Number"])).strip()]
                    # concat the street parts filtering out blank parts
                    land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()
                else:
                    land_info["physical_address"] = " ".join(str(row["Address"]).upper().split())

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                for i in range(1,3):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:

                        land_info["sale_date"] = str(parser.parse(row[f"Sales_Date_{i}"]))
                        land_info["sale_price"] = row[f"Total_Sales_Price_{i}"]
                        land_info["seller_name"] = " ".join(str(row[f"Seller_{i}"]).upper().replace(",", ", ").split())
                        land_info["buyer_name"] = " ".join(str(row[f"Buyer_{i}"]).upper().replace(",", ", ").split())

                        if row[f"Book_Page_{i}"] and len(row[f"Book_Page_{i}"].split("-")) == 2:
                            book_page = row[f"Book_Page_{i}"].split("-")
                            book = str(book_page[0]).strip()
                            page = str(book_page[1]).strip()

                            try:
                                if int(book) != 0 and int(page) != 0:
                                    land_info["book"] = int(book)
                                    land_info["page"] = int(page)

                            except ValueError:
                                pass

                        # Delete if no year_built
                        try:
                            if int(row[f"Year_Built_{i}"]) >= 1690 and int(row[f"Year_Built_{i}"]) <= 2022:
                                land_info["year_built"] = row[f"Year_Built_{i}"]

                        except ValueError:
                            pass

                        year = land_info["sale_date"].split("-")[0]
                        month = land_info["sale_date"].split("-")[1]

                        if int(year) < 2022:
                            if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "":
                                writer.writerow(land_info)
                        elif land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) == 2022 and int(month) <= 3:
                            writer.writerow(land_info)

                    except parser._parser.ParserError:
                        continue


            except parser._parser.ParserError:
                pass
