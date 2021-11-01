import pandas as pd

df = pd.read_csv("BusinessInfo.txt",delimiter="\t")

df.to_csv("BusinessInfo.csv", encoding='utf-8', index=False)
