import pandas as pd
import os
from tqdm import tqdm

in_dir = "./downloads/"
out_dir = "./output_files/"
for file in tqdm(os.listdir(in_dir)):
    df = pd.read_json(os.path.join(in_dir, file), orient='records', dtype=str)
    df.to_csv(os.path.join(out_dir, file.split(".")[0] + ".csv"), index=False)
