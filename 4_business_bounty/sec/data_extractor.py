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
                if loaded_json["entityType"] == "operating":
                    print("   [*] Entity is active!")

                    business_info = {}

                    sic4 = loaded_json["sic"]
                    ein = loaded_json["ein"]
                    website = loaded_json["website"]
                    state_registered = loaded_json["stateOfIncorporation"]

                    mailing_address = loaded_json["mailing"]
                    street1 = mailing_address["street1"]
                    street2 = mailing_address["street2"]

                    city = mailing_address["city"]
                    state = mailing_address["StateOrCountry"]
                    zipcode = mailing_address["zipCode"]

                    if "-" in zipcode:
                        zipcode = zipcode.split("-")[0]

                    

                elif loaded_json["entityType"] == "other":
                    print("   [*] Entity is not active!")
                else:
                    with open("entityType.txt", "a", newline="") as fail_file:
                        fail_file.write(str(loaded_json["entityType"]) + "\n")
