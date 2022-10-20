import pandas as pd
import numpy as np

# "SitusCity","SitusAddress",,"ClassCodeUse","DeedBook","DeedPage","YearBuilt","SitusZipcode",
# "LegalAcres","SaleDate","SaleAmount"
df = pd.read_csv("Parcels.csv", dtype={"SitusZipcode": "object"})

df = df.drop(
    [
        "LastUpdateDate",
        "LegalTownship",
        "SitusState",
        "X",
        "Y",
        "OBJECTID",
        "GeographicalLocation",
        "SitusNumber",
        "SitusDirection",
        "SitusStreet",
        "SitusStreetType",
        "SitusState",
        "FullSitusAddress",
        "OwnerName1",
        "OwnerName2",
        "OwnerAddress1",
        "OwnerAddress2",
        "OwnerCity",
        "OwnerState",
        "OwnerZip",
        "LegalDescription",
        "LegalSection",
        "LegalRange",
        "LegalDirection",
        "ClassCodeStatus",
        "MobileHome",
        "StateTaxabilityCode",
        "Neighborhood",
        "NeighborhoodDescription",
        "CountyArea",
        "TaxingDistrict",
        "DistrictDescription",
        "SchoolDistrict",
        "Usability",
        "AppraisalID",
        "Condition",
        "Quality",
        "Shape__Area",
        "Shape__Length",
        "BuildingCostNew",
        "PropertyValue",
        "LandValue",
        "IOLL",
        "Built",
        "ClassCodeZoning",
        "ClassCodeLocation",
        "ClassCodeCitySize",
        "ClassCodeParcSize"
    ], axis=1
)

df = df.rename(columns={
    "PID": "property_id",
    "SitusCity": "property_city",
    "SitusAddress": "property_street_address",
    "ClassCodeUse": "property_type",
    "DeedBook": "book",
    "DeedPage": "page",
    "YearBuilt": "building_year_built",
    "SitusZipcode": "property_zip5",
    "LegalAcres": "land_area_acres",
    "SaleDate": "sale_datetime",
    "SaleAmount": "sale_price"

})
# ClassCodeUse types
class_type = {
    3: "commercial",
    1: "single family residential",
    5: "agriculture",
    11: "commercial",
    6: "agriculture",
    10: "commercial",
    4: "industrial",
    12: "commercial",
    9: "industrial",
}

df["property_type"] = df["property_type"].map(class_type)

print(len(df))
df = df.dropna(subset=["sale_datetime"])
print(len(df))

df["property_street_address"] = df["property_street_address"].apply(lambda x: " ".join(str(x).upper().split()).strip())
df["source_url"] = df["property_id"].apply(lambda x: f"https://nebraskaassessorsonline.us/vendors.aspx?county=20&parcel={x}" + "&vid={7970EBA7-8E15-4A19-A7B4-F8B98241DAC8}")
df["sale_datetime"] = pd.to_datetime(df["sale_datetime"], unit="ms")

df["property_county"] = "CASS"
df["state"] = "NE"

df["building_year_built"] = np.where(df["building_year_built"] > 1492, df["building_year_built"], pd.NA)

df.to_csv("extracted_data.csv", index=False)
