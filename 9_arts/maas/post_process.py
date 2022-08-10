import pandas as pd

df = pd.read_csv("combined.csv")

df['drop_me'] = df["drop_me"].apply(lambda x: "https://collection.maas.museum/object/" + str(x))
df.rename(columns={"drop_me":"source_2"}, inplace=True)
df.to_csv("finished.csv", index=False)
