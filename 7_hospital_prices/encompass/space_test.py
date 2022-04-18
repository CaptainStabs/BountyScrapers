import pandas as pd
df = pd.read_csv('62-1178229_Encompass Health Lakeshore Rehabilitation Hospital_standardcharges.csv', skiprows = 5, encoding = "latin", dtype="str")
df.columns = [col.strip('negotiated charge').strip() for col in df.columns]
df = df.rename(columns = {
    'GROSS_CHARGE':'GROSS CHARGE',
    'DISCOUNTED_CASH_PRICE':'CASH PRICE',
    'BILLING_REVENUE_SERVICE_CODE':'code',
    'ITEM_SERVICE_PACKAGE':'description',
    'PATIENT_TYPE':'inpatient_outpatient',
    'DEIDENTIFIED_MIN_NEGOTIATED_CHARGE':'MIN',
    'DEIDENTIFIED_MAX_NEGOTIATED_CHARGE':'MAX',
})
df['code'] = df['code'].apply(lambda x: [y.strip() for y in str(x).split(';')])
df = df.explode('code')
df = df.melt(id_vars = df.columns[:3], value_vars = df.columns[3:], var_name = 'payer', value_name = 'price')
df = df[df.price.str.contains('\$', na=False)]
df['price'] = df['price'].str.strip('$')

df.to_csv("space.csv")
