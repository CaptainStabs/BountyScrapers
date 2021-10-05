import json
from tqdm import tqdm
import csv
from utils.interrupt_handler import GracefulInterruptHandler

dir = "E:\\submissions\\"
filename = "data.csv"

columns = ["name", "business_type", "state_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "ein", "sic4", "website"]
with open(filename, "a", encoding="utf-8", newline="") as output:
    with GracefulInterruptHandler() as h:
        writer = csv.DictWriter(output, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for root, dirs, files in os.walk(dir):
            for file in files:
                if "-submissions-" not in file:
                    if h.interrupted:
                        print("   [!] Interrupted, exiting.")
                        break

                    loaded_json = json.load(file)
                    if loaded_json["entityType"] == "operating":
                        print("   [*] Entity is active!")

                        business_info = {}
                        name = loaded_json["name"]
                        cik = loaded_json["cik"]
                        business_info["filing_number"] = "CIK" + str(cik).zfill(10)
                        business_info["sic4"] = loaded_json["sic"]
                        business_info["ein"] = loaded_json["ein"]
                        business_info["website"] = loaded_json["website"]
                        business_info["state_registered"] = loaded_json["stateOfIncorporation"]

                        business_info["name"] = name

                        business_address = loaded_json["business"]
                        street1 = business_address["street1"]
                        street2 = business_address["street2"]

                        if street1 == "null":
                            add_street1 = False
                        else:
                            add_street1 = True

                        if street2 == "null":
                            add_street2 = False
                        else:
                            add_street2 = True

                        if add_street1 and add_street2:
                            business_info["address_physical"] = str(street1).strip() + " " + str(street2).strip()
                        elif add_street1 and not add_street2:
                            business_info["address_physical"] = add_street1
                        elif not add_street1 and add_street2:
                            business_info["address_physical"] = add_street2

                        business_info["city_physical"] = business_address["city"]
                        business_info["state_physical"] = business_address["StateOrCountry"]
                        zip5_physical = business_address["zipCode"]

                        if "-" in zip5_physical:
                            business_info["zip5_physical"] = zip5_physical.split("-")[0]

                        business_type_string = name

                        if "COOPERATIVE" in business_type_string:
                            business_info["business_type"] = "COOP"
                            print("      [?] Translated type 1: COOP")

                        if "COOP " in business_type_string:
                            business_info["business_type"] = "COOP"
                            print("      [?] Translated type 2: COOP")
                        if "CORP" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 1: CORPORATION")

                        if "CORP " in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 2: CORPORATION")

                        if "CORPORATION" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 3: CORPORATION")

                        if "DBA" in business_type_string:
                            business_info["business_type"] = "DBA"
                            print("      [?] Translated type: DBA")

                        if "LIMITED LIABILITY COMPANY" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 1: LLC")

                        if "LLC" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 2: LLC")

                        if "L.L.C." in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 3: LLC")

                        if "L.L.C" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translated type 4: LLC")

                        if "NON-PROFIT" in business_type_string:
                            business_info["business_type"] = "NONPROFIT"
                            print("      [?] Translated type 1: NON-PROFIT")

                        if "NONPROFIT" in business_type_string:
                            business_info["business_type"] = "NONPROFIT"
                            print("      [?] Translated type 2: NONPROFIT")

                        if "PARTNERSHIP" in business_type_string:
                            business_info["business_type"] = "PARTNERSHIP"
                            print("      [?] Translated type: PARTNERSHIP")

                        if "SOLE PROPRIETORSHIP" in business_type_string:
                            business_info["business_type"] = "SOLE PROPRIETORSHIP"
                            print("      [?] Translated type: SOLE PROPRIETORSHIP")

                        if "TRUST" in business_type_string:
                            business_info["business_type"] = "TRUST"
                            print("      [?] Translated type: TRUST")

                        if "INC " in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 1: INC")

                        if "INC" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 2: INC")

                        if "INCORPORATED" in business_type_string:
                            business_info["business_type"] = "CORPORATION"
                            print("      [?] Translated type 3: INC")

                        # if "LIMITED" in business_type_string:
                        #     business_info["business_type"] = "LTD"
                        #     print("      [?] Translaetd type1: LTD")

                        if "LTD" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translaetd type 2: LLC")

                        if "L.T.D" in business_type_string:
                            business_info["business_type"] = "LLC"
                            print("      [?] Translaetd type 3: LLC")

                        try:
                            if not business_info["business_type"]:
                                business_info["business_type"] = "CORPORATION"

                        except ValueError:
                            print("   [!] ValueError!")
                            business_info["business_type"] = "CORPORATION"

                        writer.writerow(business_info)




                    elif loaded_json["entityType"] == "other":
                        print("   [*] Entity is not active!")
                    else:
                        with open("entityType.txt", "a", newline="") as fail_file:
                            fail_file.write(str(loaded_json["entityType"]) + "\n")
