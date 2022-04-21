import mysql.connector
import functools

@functools.lru_cache(maxsize=None)
def jail_name_search(jail_name, state, conn, split=True):
    b = jail_name
    if split:
        jail_name = " ".join(jail_name.split()[:2])
    else:
        jail_name = jail_name

    cursor = conn.cursor()
    cursor.execute(f"SELECT id from jails where facility_name like '{jail_name}%' and facility_state in ('{state}');")
    id = list()
    for r in cursor:
        id.append(r)

    if len(id) > 1:
        print("\nTOO MANY IDS:", id, b)

    elif not len(id):
        # print("NOTHING FOUND:", id, jail_name)
        a = "a"

    else:
        id = id[0][0]
        return id
