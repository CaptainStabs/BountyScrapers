import pandas as pd


# ,RPC,LocAddr,LocCity,,LocZip,LegalAc,,Sale1D,Sale1Amt,Doc1Ref,Doc2Ref,Doc3Ref,instnum1,instnum2,instnum3,Grantor1
#,Elec,Gas,Water,Sewer,StreetSD,NumDwlg,NumOth,NumImp,yrbuilt,SqFT
df = pd.read_csv("parcels.csv")

df = df.drop([
    "OBJECTID",
    "LINK",
    "LRSNum",
    "Owner1",
    "Owner2",
    "MailAddr",
    "MailAddr2",
    "MailCity",
    "MailStat",
    "MailZip",
    "TaxAcct",
    "Legal1",
    "LandVal1",
    "DwlgVal1",
    "OthVal1",
    "TotVal1",
    "Grantor1",
    "Elec",
    "Gas",
    "Water",
    "Sewer",
    "StreetSD",
    "NumDwlg",
    "NumOth",
    "LocState",
    "instnum2",
    "instnum3",
    "Doc1Ref",
    "Doc2Ref",
    "Doc3Ref",
], axis=1)

df = df.rename(columns={
    "RPC": "property_id",
    "LocAddr": "property_street_address",
    "LocCity": "property_city",
    "LocZip": "property_zip5",
    "LegalAc": "land_area_acres",
    "Sale1D": "sale_datetime",
    "Sale1Amt": "sale_price",
    "instnum1": "sale_id",
    "NumImp": "building_num_units",
    "yrbuilt": "building_year_built",
    "SqFT": "building_area_sqft"

})
df["source_url"] = df["property_id"].apply(lambda x: f"https://www.webgis.net/va/botetourtco/?op=id&id=1|parcels|RPC|{x}")

df["sale_datetime"] = pd.to_datetime(df["sale_datetime"], unit="ms")

# df[["book", "page"]] = df["Doc1Ref"].apply(lambda x: x.split("") if " " in x else pd.NA)
# df["Doc1Ref"].apply(lambda x: print(type(x)))
                       # df.apply(lambda x: date_checker(x["production_dates"], x["date_description"]), axis=1, result_type="expand")
print(df.columns)
print(df)

df["state"] = "VA"
df["property_county"] = "BOTETOURT"
df["property_zip5"] = df["property_zip5"].apply(lambda x: str(x).split("-")[0] if "-" in str(x) else x)
df.loc[df['property_zip5'].str.len()>5,'property_zip5'] = pd.NA
df.loc[df['property_zip5'].str.len()<5,'property_zip5'] = pd.NA

df = df.dropna(subset=["property_street_address", "sale_datetime"])
df.to_csv("extracted_data.csv", index=False)
# # https://www.webgis.net/va/botetourtco/?op=id&id=1|parcels|RPC|29060
