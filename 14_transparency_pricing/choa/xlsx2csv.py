import pandas as pd


file = 'input_files\\58-0572412_Childrens_Healthcare_of_ATL_at_Egleston_standardcharges.xlsx'
df = pd.read_excel(file, skiprows=1, dtype={'Code': str, 'Procedure': str, 'NDC': str, 'Rev Code': str})
df.to_csv(file.replace(".xlsx", '.csv'), index=False)