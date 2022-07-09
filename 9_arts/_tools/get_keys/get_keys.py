import argparse

def get_keys(file):
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
                str_list.append(line.strip().replace('"', "").split(":")[0])

    print(str_list)

def cli():
    parser = argparse.ArgumentParser(description='Get keys from data dictionary')
    parser.add_argument('file', type=str, metavar='FILE', help='Path to input script')
    args = parser.parse_args()
    get_keys(args.file)


if __name__ == "__main__":
    cli()
