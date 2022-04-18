import csv
import os
import json
import doltcli as dolt
import requests
import googlesearch as google
from urllib.parse import urlparse
from _cookie import dolt_cookie
import re
from utils.interrupt_handler import GracefulInterruptHandler

dir = ("./submited/")  # Where the save directory should be
full_auto = True  # Default False


db = dolt.Dolt("C:\\Users\\adria\\hospital-price-transparency-v3")  # Select the dolt database


def check_if_exists(headers):
    with GracefulInterruptHandler() as h:
        file = "F:\\"
        branch_name = "encompassHospitals"
        db.checkout(branch=branch_name)
        if ".csv" in file:                               # We only want the CSVs
            with open(root + file, 'r') as f:
                read_csv = csv.DictReader(f)
                print("\n" + file)
                success = True

                if success:  # No point in wasting time on broken files
                    # response = requests.request("POST", url, headers=headers, data=payload)  # Don't need this anymore, used to check if the branch existed in  a PR

                    try:
                        print("            [*] Trying to write to db...")
                        filename = file.replace("_"," ").lower()
                        dolt.write_file(dolt=db, table="prices", file_handle=open(root + file, "r"), import_mode="create", commit=False, do_gc=False)
                        success2 = True
                            # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                    except Exception as error:
                            print(error)
                            print("               [!] Write failure")
                            if "dolt add" in str(error):
                                print("         [!] Data was already added to database, skipping.")
                                success2 = True
                            else:
                                success2 = False
                                print("          [!] Other error, idk")
                                with open("csv_fails.txt", "a") as output:  # Log the failure
                                    output.write(file + ", " + file + ", write failure" + "\n")
                            pass

                    if success2:
                        print("      [*] Finished push, moving" )
                        f.close()  # Close to prevent in use error

                        try:
                            print("      [*] Moving file...")
                            os.rename(root + file, root + "verified_submitted/" + file)  # move the file
                        except FileExistsError:
                            print("      [!] File already exists! Removing current one.")
                            with open("removed.txt", "a") as f:
                                f.write(file + ", pr existed, file existed\n")
                            os.remove(root + file)
                            pass



                    # """Being the early stages that dolt is in, these are primarily workarounds.
                    # Due to the (mostly) autonomous nature of this script, I don't want any errors interefering with it's progress.
                    # """
                    # print("            [*] Trying to push to remote")
                    # try:
                    #     db.push(remote="origin", set_upstream=True, refspec=branch_name)
                    #     success2 = True
                    #
                    # except Exception as error:
                    #     print("         [!] " + str(error))
                    #     print("               [!] Push failed")
                    #     with open("csv_fails.txt", "a") as output:  # Log the failure for manual review
                    #         output.write(file + ", " + file + ", push failure" + "\n")
                    #     sucess2 = False
                    #     pass
                    #
                    # if success2:  # If a pr already exists for that file
                    #     print("      [*] Finished push, moving" )
                    #     f.close()  # Close to prevent in use error
                    #
                    #     try:
                    #         print("      [*] Moving file...")
                    #         os.rename(root + file, root + "verified_submitted/" + file)  # move the file
                    #     except FileExistsError:
                    #         print("      [!] File already exists! Removing current one.")
                    #         with open("removed.txt", "a") as f:
                    #             f.write(file + ", pr existed, file existed\n")
                    #         os.remove(root + file)
                    #         pass


            #
            # print(read_csv)
                        # input()

# get_open_prs(payload, headers, url)
check_if_exists(headers=headers)
