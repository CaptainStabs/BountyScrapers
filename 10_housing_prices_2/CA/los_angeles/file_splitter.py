from tqdm import tqdm

chunk_size = 275819
base = "F:\\_Bounty\\us-housing-prices-v2\\LA\\input_files\\"
def write_chunk(part, lines):
    with open('F:\\_Bounty\\LA\\input_files\\split_file_'+ str(part) +'.csv', 'w') as f_out:
        f_out.write(header)
        for line in tqdm(lines, total=275819):
            f_out.write(line)
        # f_out.writelines(lines)
with open("LA.csv", "r") as f:
    count = 0
    header = f.readline()
    lines = []
    for line in tqdm(f, total=4137293):
        count += 1
        lines.append(line)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
        # else:
    # write remainder
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)
