# import requests
# import os
# import pandas as pd
# import csv
# import sys
#
# agency_ids = ["f4c4793fe59c4d669de1e198a1733521", "cd0f6aa8523942a2a5b5d9cbb3688e10", "06ea13149a22455a9c2be1264efa388a", "08c7749aa8ed4f5ba317da3036fffc8a", "2341502d9e4642f380b4b14831c05c76", "3cd726d92ccb45b68357793072fe140d", "40cc6feb09264975a2e2a6ac3eec80b9", "4b02595214b747549de9a87e2db14ba8", "6ee7ac47abbf4640879cd473410c8bb8", "81d558933431424b8c7b08a589304c23", "8774f0fed91348339c3fbb92cc8c407b", "99256d2a51b040d78c1627eada5a44bf", "6c34515169b74d418b9bf7117c86543a"]
#
# with open("agencies2_copy.csv", "r", encoding="utf-8") as input_source:
#     df = pd.read_csv(input_source)
#     # access the dataframe columns
#     df_columns = list(df.columns)
#     # join the returned list to format as csv header
#     data_columns = ",".join(map(str, df_columns))
#
# with open("agencies_cleaned.csv", "a", encoding="utf-8") as cleaned_output:
#     for index, row in df.iterrows():
#         for i in range(len(agency_ids)):
#             if agency_ids[i] in row["id"]:
#                 if row["agency_type"] != 6:
#                     row["agency_type"] = str(6)
#         row_list = pd.Series.tolist(row)
#         row_list = ",".join(map(str, row_list))
#         cleaned_output.write(f"{row_list}\n")
