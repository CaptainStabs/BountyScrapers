import os
from tqdm import tqdm
import doltcli as dolt
import winsound

in_dir = "C:/Users/adria/github/BountyScrapers/7_hospital_prices/HCA/split_files/"

db = dolt.Dolt("C:/Users/adria/hospital-price-transparency-v4/")

for file in tqdm(os.listdir(in_dir)):
    dolt.write_file(
        dolt=db,
        table="prices",
        file=os.path.join(in_dir, file),
        import_mode="create"
    )

for i in range(50):
    winsound.Beep(random.randrange(37,3500),random.randrange(7,200))

winsound.MessageBeep(winsound.SND_ASYNC, type=winsound.MB_ICONEXCLAMATION)
