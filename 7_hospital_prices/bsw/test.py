import pandas as pd

df = pd.read_csv('extracted_data.csv', dtype=str)


# df = df.loc[df.duplicated(subset=(df.columns.difference(['inpatient_outpatient'])), keep=False)]
# print(df.duplicated(subset=(["cms_certification_num",  "internal_revenue_code", "code", "description", "payer", "price", "code_disambiguator"])))
# print(df)
print(df.duplicated())
