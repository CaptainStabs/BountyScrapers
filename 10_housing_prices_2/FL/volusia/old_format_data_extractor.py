import pyodbc
import csv
from tqdm import tqdm
import argparse
from os import system
from dateutil import parser as dateparser


# def data_extractor(year, dbq):

# dbq = f"F:\\__volusia\\databases\\CAMA_DATA_EXPORT{year}F\\CAMA_DATA_EXPORT_WEB.accdb;"

parser = argparse.ArgumentParser()
parser.add_argument('year', type=str)
parser.add_argument('dbq_type', type=int)
parser.add_argument('--custom_name', default=False, type=str)
args = parser.parse_args()

year = args.year
dbq_type = args.dbq_type

system("title " + year)


if dbq_type == 0:
    dbq = f"F:\\__volusia\\databases\\CAMA_DATA_EXPORT{year}F\\CAMA_DATA_EXPORT_WEB.accdb;"

elif dbq_type == 1:
    dbq = f"F:\\__volusia\databases\\VOLIS-ACCESS-{year} FTR\\VOLIS-ACCESS-{year} FTR.mdb;"

elif dbq_type == 2:
    dbq = f"F:\\__volusia\databases\\VOLIS-ACCESS-{year}-FTR\\VOLIS-ACCESS-{year} FTR.mdb;"

elif dbq_type == 3:
    dbq = f"F:\\__volusia\databases\\VOLIS-ACCESS-{year}-FTR\\VOLIS-ACCESS-{year}-FTR.mdb;"



if args.custom_name:
    dbq = args.custom_name


print(dbq)
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + dbq)
cursor = conn.cursor()

columns = ["state", "property_id", "sale_date", "book", "page", "sale_price", "physical_address", "city", "zip5", "source_url"]

cursor.execute("select ALT_KEY, SALE_BOOK_NBR, SALE_PAGE_NBR, SALES_PRICE, SALE_DATE from Web_Sales_View")
rows = cursor.fetchall()


with open(f"F:\\__volusia\\{year}_extracted_data.csv", "a", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for row in tqdm(rows):
        land_info = {
            "state": "FL",
            "property_id": str(row[0]).split(".")[0],
            "book": row[1],
            "page": row[2],
            "sale_price": str(row[3]).split(".")[0],
            "sale_date": row[4],

            "source_url": "https://vcpa.vcgov.org/download/database#gsc.tab=0"
        }
        print(land_info["property_id"])
        cursor.execute(f'select PARCEL_ID, SITUS_STREET_NBR, SITUS_STREET_DIRECTION, SITUS_STREET_NAME, SITUS_STREET_TYPE, SITUS_SUITE_NBR, SITUS_CITY, SITUS_ZIP_CODE from Web_Parcel_View_volcoit where ALT_KEY = {land_info["property_id"]}')

        results = cursor.fetchone()
        # print(results)

        # While I could just get the address all in one go, this makes it so that I don't have to parse
        try:
            street_list = [str(results[1]).split(".")[0]]
        except TypeError:
            street_list = [""]

        try:
            for i in range(2,5):
                if results[i] == None:
                    street_list.append("")
                else:
                    street_list.append(results[i])

            # concat the street parts filtering out blank parts
            land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())
            land_info["city"] = results[6]
            land_info["zip5"] = results[7]
            land_info["property_id"] = results[0]
            writer.writerow(land_info)

        except TypeError:
            pass
