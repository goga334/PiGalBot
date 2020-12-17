import sqlite3

con = sqlite3.connect("pigalbot_data_base.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS   
            pigalbot_users(
            id TEXT,
            name TEXT
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS   
            pigalbot_galleries(
            id TEXT,
            name TEXT
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS   
            pigalbot_pics(
            id TEXT,
            gallery TEXT,
            link TEXT
            )""")


print("Here's a listing of all the records in the pigalbot_users:")
for row in cur.execute("SELECT rowid, * FROM pigalbot_users "):
    print(row)

print(cur.fetchall())

print("Here's a listing of all the records in the pigalbot_galleries:")
for row in cur.execute("SELECT rowid, * FROM pigalbot_galleries "):
    print(row)

print(cur.fetchall())

print("Here's a listing of all the records in the pigalbot_pics:")
for row in cur.execute("SELECT rowid, * FROM pigalbot_pics "):
    print(row)


print(cur.fetchall())
con.close()


