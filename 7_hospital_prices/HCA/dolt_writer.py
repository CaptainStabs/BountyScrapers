import os
from tqdm import tqdm
import doltcli as dolt
import winsound
import random
#
# in_dir = "C:/Users/adria/github/BountyScrapers/7_hospital_prices/HCA/split_files/"
#
# db = dolt.Dolt("C:/Users/adria/hospital-price-transparency-v4/")
#
# for file in tqdm(os.listdir(in_dir)):
#     dolt.write_file(
#         dolt=db,
#         table="prices",
#         file=os.path.join(in_dir, file),
#         import_mode="create"
#     )
#
# db.commit(message="Reimport prices")
# dolt.push(remote='origin', refspec='HCA')
import datetime
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
for i in range(200):
    winsound.Beep(random.randrange(440,3500),random.randrange(70,200))

winsound.MessageBeep(type=winsound.MB_ICONEXCLAMATION)
