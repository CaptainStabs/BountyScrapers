from tqdm import tqdm

with open("F:\\us-housing-prices-2\\null_zips.csv", "r") as f:
    with open("F:\\us-housing-prices-2\\progresses_zips.csv", "a") as out_f:
        out_f.write("state,zip5,physical_address,city,county,property_id,sale_date,property_type,sale_price,seller_name,buyer_name,num_units,year_built,source_url,book,page,sale_type\n")
        f.seek(6893427)
        try:
            for line in tqdm(f, total=13657001):
                if line != "ov.opendata.arcgis.com/datasets/c518fafaabf8476fb83d5a7b7b1aa7be_0/explore,,,":
                    out_f.write(line)
        except UnicodeDecodeError:
            print(line)
