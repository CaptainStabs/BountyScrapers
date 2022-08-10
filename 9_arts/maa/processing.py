import pandas as pd
import ast


def test(x):
    try:
        if not isinstance(x, float):
            x = ast.literal_eval(x)
            return x["url"]
        else:
            return pd.NA
    except:
        print(x)
        raise
df = pd.read_csv('extracted_data.csv')

df["image_url"] = df["image_url"].apply(lambda x: test(x))
df["accession_number"] = df["accession_number"].apply(lambda x: x[:500] if isinstance(x, str) else pd.NA)
df.to_csv("cleaned_data.csv", index=False)
