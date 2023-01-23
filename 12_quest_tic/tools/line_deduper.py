import hashlib
from tqdm import tqdm

def deduplicate(file_path, output_path):
    # Create an empty set to store the unique lines
    unique_lines = set()
    # Open the file for reading
    with open(file_path, "r") as file:
        # Open the output file for writing
        with open(output_path, "a") as output_file:
            # Iterate over each line in the file
            for line in tqdm(file, total= 218817893):
                # Create a hash of the line
                line_hash = hashlib.md5(line.encode()).hexdigest()
                # If the hash is not already in the set, add it and write the line to the output file
                if line_hash not in unique_lines:
                    unique_lines.add(line_hash)
                    output_file.write(line)

deduplicate("F:\\_Bounty\\anthem_files.txt", "F:\\_Bounty\\anthem_deduped.txt")
