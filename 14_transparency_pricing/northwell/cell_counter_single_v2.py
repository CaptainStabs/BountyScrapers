import pandas as pd
import numpy as np
import argparse

def count_cell(file):
    df = pd.read_csv(file, low_memory=False)
    print("Rows:", len(df))
    print("Cell edits:", "{:,}".format(np.sum(df.replace('', np.nan).count())))

def cli():
    parser = argparse.ArgumentParser(description="Get a count of non-null cells")
    parser.add_argument("file", type=str, help="Path to file")
    args = parser.parse_args()
    count_cell(args.file)

if __name__ == "__main__":
    cli()
