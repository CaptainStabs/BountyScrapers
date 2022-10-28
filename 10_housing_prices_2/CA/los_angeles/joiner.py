import pandas as pd
import os

path = 'F:\\_Bounty\\LA\\'
f_list = [os.path.join(path, files) for files in os.listdir(path)]
f_list.pop(f_list.index("F:\\_Bounty\\LA\\input_files"))

df_from_each_file = (pd.read_csv(f) for f in f_list)
df = pd.concat(df_from_each_file, ignore_index=True)

# df = df.dropna(subset='sale_price', axis=1)

df.to_csv("F:\\_Bounty\LA\\combined.csv", index=False)
