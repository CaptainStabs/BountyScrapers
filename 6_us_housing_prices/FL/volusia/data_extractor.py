import pyodbc
import csv
from tqdm import tqdm

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\_Downloads\\CAMA_DATA_EXPORT_WEB.accdb;')
cursor = conn.cursor()

columns = ["state", "property_id", "sale_date", "book", "page", "sale_price", "physical_address", "city", "zip5", "source_url"]

with open("VCPA_CAMA_SALES.csv", "r") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open("2022_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            land_info = {
                "state": "FL",
                "property_id": str(row["PARID"]).split(".")[0],
                "sale_date": row["SALEDT"],
                "book": row["BOOK"],
                "page": row["PAGE"],
                "sale_price": str(row["PRICE"]).split(".")[0],
                "source_url": "https://vcpa.vcgov.org/download/database#gsc.tab=0"
            }

            cursor.execute(f'select ADRNO, ADRADD, ADRDIR, ADRSTR, ADRSUF, ADRSUF2, UNITDESC, UNITNO, CITYNAME, ZIP1 from VCPA_CAMA_SITUS where PARID = {land_info["property_id"]}')

            results = cursor.fetchone()
            # print(results)
            try:
                street_list = [str(results[0]).split(".")[0]]
            except TypeError:
                street_list = [""]

            try:
                for i in range(1,8):
                    if results[i] == None:
                        street_list.append("")
                    else:
                        street_list.append(results[i])

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())
                land_info["city"] = results[6]
                land_info["zip5"] = results[7]
                writer.writerow(land_info)

            except TypeError:
                pass
