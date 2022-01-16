import pyodbc
import csv
from tqdm import tqdm

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\_Downloads\\CAMA_DATA_EXPORT_WEB.accdb;')
cursor = conn.cursor()

columns = ["state", "property_id", "sale_date", "book", "page", "sale_price", "physical_address", "city", "zip5", "source_url"]

cursor.execute("select PARID, SALEDT, BOOK, PAGE, PRICE from VCPA_CAMA_SALES")
rows = cursor.fetchall()


with open("2022_extracted_data.csv", "a", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for row in tqdm(rows):
        land_info = {
            "state": "FL",
            "property_id": str(row[0]).split(".")[0],
            "sale_date": row[1],
            "book": row[2],
            "page": row[3],
            "sale_price": str(row[4]).split(".")[0],
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
