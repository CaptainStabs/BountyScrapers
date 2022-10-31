import pandas as pd
import numpy as np

# df = pd.read_csv("extracted_sales_data.csv")
df = pd.read_csv("fixed_part_1.csv")


df["state"] = "CO"
df["property_county"] = "SUMMIT"
df["sale_price"] = df["sale_price"].str.replace("$", "")
df["sale_price"] = df["sale_price"].str.replace(",", "")
df["building_year_built"] = np.where(df["building_year_built"] > 1492, df["building_year_built"], pd.NA)
# df["property_street_address"] = df["property_street_address"].str.strip()
df = df.dropna(subset=["property_street_address"], axis=0)
df.to_csv("fixed_sales.csv", index=False)
