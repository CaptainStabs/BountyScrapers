with open("extracted_data_cms_certification_num_freq.csv", "r") as f:
    lines = []

    for line in f:
    	if line.strip():
            lines.append(line.strip("\n"))

print(lines)
