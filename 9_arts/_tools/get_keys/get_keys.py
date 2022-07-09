import re
import argparse

def get_keys(file):
    key_pat = re.compile(r'"(.*?)":')

    str_list = []
    copy = False
    with open(file, "r") as f:
        for line in f:
            if "data = {" in line:
                copy = True
                continue
            elif "}" in line:
                copy = False
                continue
            elif copy:
                str_list.append(line.strip())

    dic = " ".join(str_list)
    print(re.findall(key_pat, dic))

def cli():
    parser = argparse.ArgumentParser(description='Get keys from data dictionary')
    parser.add_argument('file', type=str, metavar='FILE', help='Path to input script')
    args = parser.parse_args()
    get_keys(args.file)


if __name__ == "__main__":
    cli()
