import pandas as pd
import os


path = '.\\output_files\\'
f_list = [os.path.join(path, f) for f in os.listdir(path)]

df_from_files = (pd.read_csv(f, dtype={'hospital_ccn':str}) for f in f_list)
df = pd.concat(df_from_files, ignore_index=True)

df.to_csv('combined.csv', index=False)