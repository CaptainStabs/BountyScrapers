# with open("done_files.txt", "a", newline="\n") as f:
#     for i in range(1, 16):
#         with open(f"C:\\Users\\adria\\Downloads\\diffs\\new-project ({i}).csv", "r") as in_file:
#             for line in in_file:
#                 if "https://" in line or "http://" in line:
#                     f.write(str(line) + "\n")

import pandas as pd

# df1 = pd.read_csv("UHC_payers_deduped_sorted.csv")
df1 = pd.read_csv("anthem_payers_sorted.csv")
# df2 = pd.read_csv("anthem_finished_files.txt")#["url"]

# Only for anthem because not all files are actually imported
dfa = pd.read_csv("anthem_finished_files.txt")#["url"]
dfb = pd.read_csv("anthem_my_finished.csv")["url"]
df2 = pd.concat([dfa, dfb])



# df = pd.concat([df1, df2]).drop_duplicates(keep=False)
df = df1[~df1["url"].isin(df2["url"])]
print(len(df1))
print(len(df))
df = df.sort_values(by=["size"])
df.to_csv("anthem_completed_removed.csv", index=False)
