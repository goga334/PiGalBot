import sqlite3




con = sqlite3.connect("pigalbot_data_base.db")
cur = con.cursor()

# number = '334'
# money = 220


cur.execute("""CREATE TABLE IF NOT EXISTS   
            pigalbot_users(
            id TEXT,
            name TEXT, 
            gallery TEXT
            )""")

# sql = "DELETE FROM bj_logs WHERE id= '334'"
# cur.execute(sql)
#
#
# albums = [(number, money, 23, '0010010000100', 5, '0000001001000')]
# cur.executemany("INSERT INTO bj_logs VALUES (?,?,?,?,?,?)", albums)
# con.commit()


print("Here's a listing of all the records in the table:")
for row in cur.execute("SELECT rowid, * FROM pigalbot_users "):
    print(row)

print(cur.fetchall())

# sql = "SELECT id FROM bj_logs WHERE id=?"
# cur.execute(sql, ['374433247'])
# print(cur.fetchone())
con.close()


