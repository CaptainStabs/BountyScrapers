import mysql.connector
import pandas as pd
from pathlib import Path
import sys
p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))

from _common.sql_query import search_and_add

conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')
df = pd.read_csv('input_data.csv', na_values="N/A")
df = df.head()

df["id"] = df.apply(lambda x: search_and_add(x["Institution"], "PA", conn, county=x["County"], address=x["Address + Lat/Long"].replace("N/A", "").replace("\n", "").strip(',').strip()), axis=1)
