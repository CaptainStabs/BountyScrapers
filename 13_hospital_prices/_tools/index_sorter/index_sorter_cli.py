# import pandas as pd

# df = pd.read_csv("UHC_payers_sorted.csv")

# df = df.sort_values(by=["size"])

# df.to_csv("UHC_payers_deduped_sorted.csv", index=False)
import argparse
import pandas as pd

def index_sorter(args):
    df = pd.read_csv(args.input)

    df = df.sort_values(by=["size"])

    df.to_csv(args.input[:-4].replace("_sized", "") + "_sorted.csv", index=False)

def cli():
    parser = argparse.ArgumentParser(description="Sort a payer list by `size` col")
    parser.add_argument("-i", "--input", required=True, help="Path to file")
    args = parser.parse_args()

    index_sorter(args)

if __name__ == "__main__":
    cli()