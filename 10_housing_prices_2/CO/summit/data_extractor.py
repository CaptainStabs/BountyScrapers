import pandas as pd

df = pd.read_csv('combined.csv')
df = df.drop(["PPI", "AssessorDataID", "EconomicAreaCode","EconomicAreaDescription","NeighborhoodCode","NeighborhoodDescription","SubdivisionCode","SubdivisionName","Filing","Phase","PrimaryIdentifier","SecondaryIdentifier","ShortPropertyDescription","SitusAddressID","ThoroughfareID", "HouseNumber","ThoroughfareFullName","ThoroughfareName","TownCode","Abstract1","Abstract2","Abstract3","Abstract4","Abstracts","TotalAssessedLandValue","TotalAssessedImprovementValue","TotalTaxableLandValue","TotalTaxableImprovementValue","TotalTaxableValue","TotalAssessedValue","TaxYear","TaxArea","TaxAreaMills","OwnerFirstName","OwnerLastName","OwnerFullName","OwnerContactNameLine1","OwnerContactNameLine2","OwnerContactAddressLine1","OwnerContactAddressLine2","OwnerContactCity","OwnerContactState","OwnerContactPostalCode","OwnerContactPublicMailingAddr","OwnerContactTrustedMailingAddr", "PotentialBuildOutDensityUnits","ActualBuildOutDensityUnits","PotentialBuildOutDensitySqFt","ActualBuildOutDensitySqFt","SingleFamilyEquivalents","ZoningCode", "SiteAccessCode","SiteTopographyCode","SiteScenicViewCode","SiteCoverCode","SiteSewerCode","SiteWaterCode","SiteUtilityCode","MiscellaneousCharacteristics","MiscellaneousCharacteristicIDs","NumberOfStructures", "ArchitecturalStyleCode", "AdjustedYearBuilt","ImprovementGrade","ImprovementCondition","ConstructionClassification","ExteriorWallMaterial","ExteriorWallHeight","HeatType","SquareFeetLivingArea","SquareFeetUnfinished","BasementType","GarageType","NumberOfCars","GarageSquareFeet","NumberOfRooms","NumberOfLofts","NumberOfKitchens","NumberOfMasterBathrooms", "NumberOfFullBathrooms","NumberOfThreeQuarterBathrooms","NumberOfHalfBathrooms","NumberOfQuarterBathrooms", "MobileHomeTitle","FloorLevel","ImprovementPosition","CommercialUse1","CommercialUse2","CommercialUse3","CommercialUses","ExteriorCondition", "ZoningDescription"], axis=1)
#"PPI","SitusAddress",,"TownName","TotalLandAcres","TotalLandSquareFeet","","ImprovementType","NumberOfUnits",
# "YearBuilt","SquareFeet","NumberOfBedrooms","TotalBathrooms","Latitude","Longitude"

df = df.rename(columns={
    # "PPI": "property_id",
    "PropertySchedule": "property_id",
    "SitusAddress": "property_street_address",
    "TownName": "property_township",
    "TotalLandAcres": "land_area_acres",
    "TotalLandSquareFeet": "land_area_sqft",
    "ImprovementType": "property_type",
    "NumberOfUnits": "building_num_units",
    "YearBuilt": "building_year_built",
    "SquareFeet": "building_area_sqft",
    "NumberOfBedrooms": "building_num_beds",
    "TotalBathrooms": "building_num_baths",
    "Latitude": "property_lat",
    "Longitude": "property_lon",
    "ArchitecturalStyle": "building_num_stories"
})

arch_styles = {
    "Two Story": 2,
    "One Story": 1,
    "1-1/2 Story": 1.5,
    "2-1/2 Story": 2.5,
    "Three Story": 3,

}
df["building_num_stories"] = df["building_num_stories"].map(arch_styles)

df.to_csv("extracted_data.csv", index=False)
