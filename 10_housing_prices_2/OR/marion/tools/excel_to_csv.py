from pyxlsb import open_workbook
import pandas as pd
import os


directory = "C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\_Downloads"
for file in os.listdir(directory):
    print(file)
    filename = os.fsdecode(file)
    print(filename)

    try:
        if filename.endswith(".xlsb"):
            with open_workbook(directory + "\\" + filename) as wb:
                for sheetname in wb.sheets:
                    with open(f"C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\OR\\marion\\files\\{sheetname}.csv", "a", newline="") as f:
                        with wb.get_sheet(sheetname) as sheet:
                            for row in sheet.get_rows():
                                values = [str(r.v) for r in row]
                                csv_line = ','.join(values)
                                f.write(csv_line)

        elif filename.endswith(".xls"):
            df = pd.read_excel(directory + "\\" + filename, sheet_name=None)
            for key in df.keys():
                df[key].to_csv(f'C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\OR\\marion\\files\\{key}.csv')

    except Exception as e:
        print("ERRPR: ", filename)
