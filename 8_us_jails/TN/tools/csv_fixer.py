import os

in_dir = "./csvs/"
out_dir = "./cleaned_csvs/"
skip_lines = ['",,,Other,Federal,,Pre-,Pre-,Total', '"",TDOC,Local,Conv.,&,Conv.,trial,trial,Jail', '"",,,Other,Fed', '"",TDOC,Local,Conv.,&', '"",,,Other,,,Pre-,Pre-,Total', '"",TDOC,Local,Conv.,,Conv.,trial,trial,Jail']
replace_lines = ["FACILITY,Backup,Felons,Felons***,Others,Misd.,Felony,Misd.,Pop.", "FACILITY,Backup,Felons,Felons**,Others,Misd.,Felony,Misd.,Pop.", "FACILITY,Backup,Felons,Felons***,Oth"]
for file in os.listdir(in_dir):
    if os.path.exists(os.path.join(out_dir, file)):
        os.remove(os.path.join(out_dir, file))

    with open(os.path.join(in_dir, file), "r") as in_f, open(os.path.join(out_dir, file), "a") as out_f:
        for line in in_f:
            if any(x in line for x in skip_lines):
                continue
            elif any(x in line for x in replace_lines):
                out_f.write("jail,TDOC_Backup,felony,felony2,federal_offense,misdemeanor,pre_trial_felony,pre_trial_misd,total\n")
            else:
                out_f.write(line)
