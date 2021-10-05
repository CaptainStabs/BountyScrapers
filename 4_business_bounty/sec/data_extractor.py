import json
from tqdm import tqdm
from utils.interrupt_handler import GracefulInterruptHandler

dir = "E:\\submissions\\"
filename = "data.csv"

with open(filename, "a", encoding="utf-8", newline="") as output:
    with GracefulInterruptHandler() as h:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if h.interrupted:
                    print("   [!] Interrupted, exiting.")
                    break

                loaded_json = json.load(file)
                
