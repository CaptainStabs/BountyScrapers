import os
# os.environ['PATH'] += os.pathsep + r'C:\Program Files\Dolt\bin'
# print(os.environ['PATH'])

import doltcli as dolt
from doltcli import read_rows

fn = r"C:\Users\adria\hospital-price-transparency-v3"
db = dolt.Dolt(fn)

print(read_rows(dolt=db, table="prices"))
