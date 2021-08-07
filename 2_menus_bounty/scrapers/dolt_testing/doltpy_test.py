import doltcli as dolt

db = dolt.Dolt("menus")  # Select the dolt database
db.checkout(branch="add_ALAMEDA-HEALTH-SYSTEM-FAIRMONT-HOSPITAL-2")
# dolt diff master menu_items --summary
print(dolt.Dolt.sql(db, "select * from dolt_diff_menu_items limit=50", result_format="csv"))
