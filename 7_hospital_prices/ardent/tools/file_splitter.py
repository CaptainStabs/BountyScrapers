from tqdm import tqdm

chunk_size = 1989657
def write_chunk(part, lines):
    with open('./split_files/split_file_'+ str(part) +'.csv', 'w') as f_out:
        f_out.write(header)
        f_out.writelines(lines)
with open("cleaned_data.csv", "r") as f:
    count = 0
    header = f.readline()
    lines = []
    for line in tqdm(f, total=7958627):
        count += 1
        lines.append(line)
        if count % chunk_size == 0:
            write_chunk(count // chunk_size, lines)
            lines = []
    # write remainder
    if len(lines) > 0:
        write_chunk((count // chunk_size) + 1, lines)
