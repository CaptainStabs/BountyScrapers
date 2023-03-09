import argparse
import logging
from mrfutils import data_import, flatten_mrf, InvalidMRF

logging.basicConfig()
log = logging.getLogger('mrfutils')
log.setLevel(logging.DEBUG)


url = "./test/test_file_5.json"
out_dir = "testing"
codes = "./quest/week0/codes_prelim.csv"
npis = "./quest/week0/npis.csv"

if codes:
    code_set = data_import(codes)
else:
    code_set = None
if npis:
    npi_set = {int(x[0]) for x in data_import(npis)}
else:
    npi_set = None

try:
    flatten_mrf(
        loc = url,
        out_dir = out_dir,
        code_set = code_set,
        npi_set = npi_set
    )
except InvalidMRF as e:
    log.critical(e)