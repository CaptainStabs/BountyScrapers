import doltcli as dolt
import mysql.connector
# db = dolt.Dolt("C:\\Users\\adria\\us-jails\\")
#
file = "Albany County Jail.csv"
# print(" ".join(file.split()[:2]))
jail_name = " ".join(file.split()[:2])
# id = db.sql(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('NY');", result-format='dict')
# if len(id) > 1 or not int(id):
#     print(id)
# else:
#     id = id[0]["id"]
# print(id)
# print(dir(db.sql()))

conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')
cursor = conn.cursor()

cursor.execute(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('NY');")


id = list()
for r in cursor:
    id.append(r)
print(type(id))
if len(id) > 1 or not int(len(id)):
    print(id)
else:
    id = id[0][0]

print(id)
