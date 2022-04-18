with open("./tools/extracted_data_cms_certification_num_freq.csv", "r") as f:
    lines = []

    for line in f:
        if line.strip():
            lines.append(line.strip("\n"))
    lines.pop(0)
print(f"delete from prices where code like '%,%' or '%-%' and cms_certification_num in ({str(lines)[1:-1]})")
