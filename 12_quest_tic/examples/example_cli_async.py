
import argparse
import logging
from mrfutils_async import data_import, flatten_mrf, InvalidMRF

logging.basicConfig()
log = logging.getLogger('mrfutils')
log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url')
parser.add_argument('-o', '--out', default = 'out_dir')
parser.add_argument('-c', '--codes')
parser.add_argument('-n', '--npis')

args = parser.parse_args()

url = args.url
out_dir = args.out
if args.codes:
    code_set = data_import(args.codes)
else:
    code_set = None
if args.npis:
    npi_set = {int(x[0]) for x in data_import(args.npis)}
else:
    npi_set = None

import asyncio

try:
    asyncio.run(flatten_mrf(
        loc = url,
        out_dir = out_dir,
        code_set = code_set,
        npi_set = npi_set
    ))
except InvalidMRF as e:
    log.critical(e)