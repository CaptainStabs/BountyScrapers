import pandas as pd
from pandas import util

data = {
    'A': ['1','2','3','4','5'],
    'B': ['1','2','3','4','5'],
    'C': ['1','2','3','4','5']
}

data1 = {
    'D': ['1','2','3','4','5'],
    'E': ['1','2','3','4','5'],
    'F': ['1','2','3','4','5']
}

df = [pd.DataFrame(data).set_index('A', axis=0), pd.DataFrame(data1)]

print(df)
