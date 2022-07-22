import pandas as pd
import os

path = './files/'
f_list = [os.path.join(path, files) for files in os.listdir(path)]

df_from_each_file = (pd.read_csv(f) for f in f_list)
df = pd.concat(df_from_each_file, ignore_index=True)

df["description"] = df["description"][:10000]

# df.loc[df['maker_death_year'] == '|', 'maker_death_year'] = pd.NA

df.to_csv("combined.csv", index=False)
