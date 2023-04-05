from pathlib import Path
from urllib.parse import urlparse
import re

param_expr = re.compile(r"(?<==)[^=]+(?=\.json\.gz)")

urls = [
    "https://developers.humana.com/Resource/DownloadPCTFile?fileType=innetwork&fileName=2023-02-19_20_in-network-rates_114518.json.gz",
    "https://anthembcbsoh.mrf.bcbs.com/2023-03_415_63B0_in-network-rates.json.gz?&Expires=1681999223&Signature=Mv2xVWQyeHQwgkzM6XH9xVnZfDO9Odov~4i9MID1IOlx~shNi1bkaVv7FlXi~h~XyJUSgEbm3M-Urao~7kVBBz1IWnDXP9HvonIwX2~ouP2~~QamLR6ZQrMdCvfKp5dBW-ZZ4F~hLqag4ZSaOmilD6iD53c0YBQyS0jJKvBUki8VJndH3ZuzAtWyWQows7TE5glWMrsYGcxV8c0HvoNAlwHwl5LZg6TTlwt0upWH9exhJ6YY7vHpmwUl8XfKK2mp4g8kKrYPe7QrNP9fFjzB8XL8dBirUEpRAJV0ThHRcfX42Imedo8sIGV1FjrOobCDhGlst8nekOTMXZZuo6cLxA__&Key-Pair-Id=K27TQMT39R1C8A"
]

for url in urls:
    parsed_url = urlparse(url)
    suffix = ''.join(Path(parsed_url.path).suffixes)
    if suffix:
        filename = Path(url).stem.split('.')[0]
    else:
        filename = re.search(param_expr, parsed_url.query).group(0)

    print(filename)
    

def extract_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    suffix = ''.join(Path(parsed_url.path).suffixes)
    if suffix:
        filename = Path(url).stem.split('.')[0]
    else:
        filename = re.search(param_expr, parsed_url.query).group(0)

    print(filename)