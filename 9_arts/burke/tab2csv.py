import pandas as pd

file = "UWBM_20220707-095902.txt"
df = pd.read_csv(file, sep="\t")
df.to_csv("".join([file[:-4], ".csv"]), index=False)

print(df)
