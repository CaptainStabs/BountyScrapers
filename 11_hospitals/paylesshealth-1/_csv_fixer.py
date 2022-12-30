import pandas as pd

filename = "common_paths.csv"
df = pd.read_csv(filename, dtype={'ccn':'str'})

# df = df.dropna(subset=['chargemaster_indirect_url'])
# df = df.loc[df['homepage_url'] != "https://pamhealth.com/"]
df.to_csv(filename[:-4] + "_fixed_1.csv", index=False)
