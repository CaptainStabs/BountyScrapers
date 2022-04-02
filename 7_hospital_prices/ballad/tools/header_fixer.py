import os
from tqdm import tqdm

in_dir = "./output_files/"
out_dir = "./fixed/"

for file in tqdm(os.listdir(in_dir)):
    with open(os.path.join(in_dir, file), "r") as f:
        with open(os.path.join(out_dir, file), "a") as out_f:
            for i, line in enumerate(tqdm(f)):
                if i == 0:
                    if "Procedure Description" in line:
                        line = line.split("Procedure Description")

                    elif "ProcedureDescription" in line:
                        line = line.split("ProcedureDescription")

                    elif ",Description," in line:
                        line = line.split("Description")

                    if file != "540544705_Johnston Memorial Hospital_StandardCharges_20220214 (1).csv":
                        fixed_line = "Procedure,CodeType,CPT,NDC,Charge Code,Rev Code,Quantity,Gross IP Price,Gross OP Price,ProcedureDescription" + line[1]
                    else:
                        fixed_line = "Procedure,CodeType,CPT,MCR,NDC,Charge Code,Rev Code,Quantity,Gross IP Price,Gross OP Price,ProcedureDescription" + line[1]

                else:
                    fixed_line = line

                out_f.write(fixed_line)
