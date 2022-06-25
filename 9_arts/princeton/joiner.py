import pandas as pd
import os

path = './files/'
f_list = [os.path.join(path, files) for files in os.listdir(path)]

df_from_each_file = (pd.read_csv(f) for f in f_list)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
df = concatenated_df.drop("drop_me", axis=1)
df["inscription"] = df.apply(lambda x: str(x["inscription"])[:4000], axis=1)
df["inscription"] = df["inscription"].replace("\n", "")
df.to_csv("combined.csv", index=False)
