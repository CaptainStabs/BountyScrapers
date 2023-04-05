from mrfutils.flatteners import toc_file_to_csv
import argparse
import os


def main(args):
    if not os.path.exists(args.out):
        os.makedirs(args.out)
    toc_file_to_csv(url=args.url, file=args.file, out_dir=args.out + "\\" + "1\\")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str)
    parser.add_argument('-f', '--file', type=str, default=None)
    parser.add_argument('-o', '--out', type=str)
    args = parser.parse_args()
    main(args)