import os

def field_extractor(directory):
    """Extract fields from csv files in all sub directories of given directory."""
    fields = []

    for root, dirs, files in os.walk(directory):
        # print(files)
        for file in files:
            if file.endswith(".csv") and "extracted" not in file:
                filename = f"{root}/{file}"
                # print(filename)
                f = open(filename, "r")
                try:
                    first_line = f.readline()
                except UnicodeDecodeError as exception:
                    print("Filename failed to decode: ", filename)
                    pass

                for first_line in first_line.split(","):
                    # if first_line not in fields:
                    fields.append(first_line.replace('"', "").upper().strip().replace(" ", "_"))

    with open("fields2.txt", "a") as save_fields:
        for field in fields:
            save_fields.write(f"{field}\n")

field_extractor("F:\\.TEMP\\")
