import pandas as pd

file = "Archeology.csv"
df = pd.read_csv(file)

df = df["Archive" not in df.SubCollection]


df["technique"] = df[]
