from mrfutils.flatteners import import_csv_to_set, in_network_file_to_csv
import argparse


def main(args):
	in_network_file_to_csv(url=str(args.url), out_dir=args.out, file=args.file, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str)
    parser.add_argument('-f', '--file', type=str, default=None)
    parser.add_argument('-o', '--out', type=str)
    args = parser.parse_args()
    main(args)