import pandas as pd
import numpy as np

df = pd.read_csv("finished.csv")
print(np.sum(df.replace('', np.nan).count()))
