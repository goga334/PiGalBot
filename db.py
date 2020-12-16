import sqlite3



def get_id(user_id):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT id FROM pigalbot_users WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchone()

def get_gallery(user_id):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT money FROM pigalbot_users WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]



def add_user(id, name):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(id, name)]
    cur.executemany("INSERT INTO pigalbot_users VALUES (?, ?)", albums)
    con.commit()

def add_gallery(id, gallery_name):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(gallery_name, id)]
    cur.executemany("INSERT INTO pigalbot_galleries VALUES (?, ?)", albums)
    con.commit()

def add_pics(pic_id, gallery_id):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(pic_id, gallery_id)]
    cur.executemany("INSERT INTO pigalbot_pics VALUES (?, ?)", albums)
    con.commit()

def restart(user_id):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE pigalbot_users 
        SET money = 100
        WHERE id = ?
        """
    cur.execute(sql, [user_id])
    con.commit()



def logs ():
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    result = ""
    print("Here's a listing of all the records in the table:")
    for row in cur.execute("SELECT rowid, * FROM pigalbot_users "):
        result += str(row)+'\n'

    return result
