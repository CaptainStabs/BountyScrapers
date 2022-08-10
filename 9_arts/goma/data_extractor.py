import pandas as pd

df = pd.read_csv("qagoma-collection-as-at-30-june-2021.csv")

df = df.drop(["ecatalogue_key", "PhySupport", "SummaryData", "EdiEditionNotes"], axis=1)

df.columns = ["object_number", "department", "maker_full_name", "title", "date_description", "materials", "dimensions", "credit_line", "accession_number"]

df["source_1"] = "https://www.data.qld.gov.au/dataset/qagoma-collection/resource/f186f5b6-16d1-4bfe-9b90-f73fc5fef9e7"
df["institution_name"] = "Gallery of Modern Art"
df["institution_city"] = "South Brisbane"
df["institution_state"] = "Queensland"
df["institution_country"] = "Australia"
df["institution_latitude"] = -27.470274408384327
df["institution_longitude"] = 153.0170475669178

df.to_csv("extracted_data.csv", index=False)
