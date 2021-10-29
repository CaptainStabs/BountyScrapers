import pandas as pd

id_list = []
for i in range(1,6): # Open alabama(x).csv
    df = pd.read_csv(f"alabama{i}.csv")
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    # Get the last row from df
    last_row = df.tail(1)
    # Access the corp_id
    last_id = last_row["corp_id"].values[0]
    id_list.append(last_id)
