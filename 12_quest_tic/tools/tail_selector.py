import tailer
import pandas as pd
import io

with open("F:\\_Bounty\\payers.csv") as f:
    last_lines = tailer.tail(f, 200)

df = pd.read_csv(io.StringIO('\n'.join(last_lines).replace(",", "")), header=None)

df.to_csv("last_200.csv", index=False)
