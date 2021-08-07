
from validate_nutrition import *
import doltcli
from validate_pks import *
import sys

relative_path_to_dolt_directory = "./menus"
db = doltcli.Dolt(relative_path_to_dolt_directory)

def main():
  args = sys.argv
  if len(args) < 2:
    print("Pass 'as of' commit hash as argument to script")
  asOf = sys.argv[1]

  rows = doltcli.read_rows_sql(db, f"SELECT * FROM menu_items as of {asOf!r}")
  for row in rows:
    validatePks(row)
    validateNutrition(row)

main()
