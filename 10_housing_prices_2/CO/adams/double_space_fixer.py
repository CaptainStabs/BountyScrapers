from tqdm import tqdm

# open "combined.csv" in read mode as f
with open("combined.csv", "r") as f:
    with open("cleaned_combined.csv", "a", newline="") as f_out:
        for line in tqdm(f):
            line = " ".join(line.split()).strip()
            f_out.write(line+"\n")
