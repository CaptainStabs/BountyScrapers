import pandas as pd
import os


def get_last_id(filename, size=250, col_name="drop_me"):
    if os.path.exists(filename) and os.stat(filename).st_size > size:
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row[col_name].values[0]
        last_id += 1
        return last_id
    else:
        last_id = 1
        return
