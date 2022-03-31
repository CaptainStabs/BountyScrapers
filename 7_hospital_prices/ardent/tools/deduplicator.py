from tqdm import tqdm
seen = set()
with open("extracted_data.csv", "r") as f:
    with open("cleaned_data.csv", "a") as out_f:
        for line in tqdm(f, total=49727623):
            h = hash(line)
            if h not in seen:
                out_f.write(line)
                seen.add(h)
print(len(seen))
print(len(str(seen)))
