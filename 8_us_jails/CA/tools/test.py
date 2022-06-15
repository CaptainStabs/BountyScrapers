import mysql.connector

conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='us_jails')
cursor = conn.cursor()

with open("tabula-Tpop1d2201.csv", "r") as f:
    for line in f:
        line = line.split(" (")[0].strip('"')
        print(line)
        cursor.execute(f'''SELECT count(*) from jails where facility_name like "{line}%" and facility_state in ("CA");''')
        t = 0
        for r in cursor:
            t += 1

        print(t)
