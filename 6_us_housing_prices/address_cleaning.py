import csv
from tqdm import tqdm

columns = ['state', 'zip5', 'physical_address', 'city', 'county', 'property_id', 'sale_date', 'property_type', 'sale_price', 'seller_name', 'buyer_name', 'num_units', 'year_built', 'source_url', 'book', 'page']


def remove_double_space():
    with open("buyer_name_cleaning.csv", "r") as input_csv:
        csv_reader = csv.DictReader(input_csv)

        with open("buyer_name_cleaned.csv", "a", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=columns)
            writer.writeheader()

            for row in tqdm(csv_reader):
                land_info = {
                    "state": row['state'],
                    "zip5": row['zip5'],
                    "physical_address": " ".join(row['physical_address'].upper().split()).strip(),
                    "city": " ".join(row['city'].split()).strip(),
                    "county": " ".join(row['county'].split()).strip(),
                    "property_id": row['property_id'],
                    'sale_date': row['sale_date'],
                    'property_type': " ".join(row['property_type'].split()).strip(),
                    'sale_price': row['sale_price'],
                    'seller_name': " ".join(row['seller_name'].split()).strip(),
                    'buyer_name': " ".join(row['buyer_name'].split()).strip(),
                    'num_units': row['num_units'],
                    'year_built': row['year_built'],
                    'source_url': row['source_url'],
                    'book': row['book'],
                    'page': row['page']
                    }

                writer.writerow(land_info)

remove_double_space()
