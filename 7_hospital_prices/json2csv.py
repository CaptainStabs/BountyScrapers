import pandas as pd

df = pd.read_json("Northwell_Health_Machine_Readable_File.json", orient='records', dtype=str)
df.to_csv('mrf.csv', index=False)
