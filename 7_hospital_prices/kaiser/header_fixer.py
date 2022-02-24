import os
from tqdm import tqdm

directory = ("C:\\Users\\adria\\github\\BountyScrapers\\7_hospital_prices\\kaiser\\output_files\\CDM")
output_dir = "C:\\Users\\adria\\github\\BountyScrapers\\7_hospital_prices\\kaiser\\fixed\\"
def header_fixer(directory, output_dir, header)
for file in tqdm(os.listdir(directory)):
    print(os.path.join(directory, file))
    with open(os.path.join(directory, file), "r") as f:
        with open(os.path.join(output_dir, file), "a") as out_f:
            for i, line in enumerate(f):
                if i < 5:
                    continue
                if i == 5:
                    out_f.write('"Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge ,Hospital Inpatient / Outpatient / Both')

                out_f.write(line)
