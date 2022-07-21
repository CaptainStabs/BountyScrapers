import pandas as pd
import os

path = './files/'
f_list = [os.path.join(path, files) for files in os.listdir(path)]

df_from_each_file = (pd.read_csv(f) for f in f_list)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df["drop_me"] = concatenated_df["drop_me"].astype(int)
concatenated_df = concatenated_df.drop(["title.1", "date_description.1"], axis=1)
concatenated_df.to_csv("combined.csv", index=False)
