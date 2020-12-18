import sqlite3


def get_id(user_id):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT id FROM pigalbot_users WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchone()


def gallery_list(id):
    result = []
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT name FROM pigalbot_galleries WHERE id=?"
    for row in cur.execute(sql, [id]):
        result.append(row)
    return result


def check_gallery(gal_name):
    result = []
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT name FROM pigalbot_galleries WHERE name=?"
    for row in cur.execute(sql, [gal_name]):
        result.append(row)
    return result


def get_gallery(gal_name):
    result = []
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    sql = "SELECT link FROM pigalbot_pics WHERE gallery=?"
    for row in cur.execute(sql, [gal_name]):
        result.append(row)
    return result


def add_gallery(id, name):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(id, name)]
    cur.executemany("INSERT INTO pigalbot_galleries VALUES (?, ?)", albums)
    con.commit()


def add_pics(id, name, link):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(id, name, link)]
    cur.executemany("INSERT INTO pigalbot_pics VALUES (?, ?, ?)", albums)
    con.commit()


def delete_gallery(name):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(name,)]
    cur.executemany("DELETE FROM pigalbot_galleries WHERE name=?", albums)
    con.commit()


def delete_pics(link):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(link,)]
    cur.executemany("DELETE FROM pigalbot_pics WHERE link=?", albums)
    con.commit()


def add(id, name):
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    albums = [(id, name)]
    cur.executemany("INSERT INTO pigalbot_users VALUES (?, ?)", albums)
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


def logs():
    con = sqlite3.connect("pigalbot_data_base.db")
    cur = con.cursor()
    result = ""
    print("Here's a listing of all the records in the table:")
    for row in cur.execute("SELECT pigalbot_users.name, pigalbot_pics.gallery, pigalbot_pics.link FROM pigalbot_pics, pigalbot_users WHERE pigalbot_pics.id = pigalbot_users.id "):
        result += str(row)+'\n'

    return result
