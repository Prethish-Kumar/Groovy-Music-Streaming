import sqlite3


def add(album_name):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS album_db(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                album_name TEXT NOT NULL,
                verified INTEGER
                )""")
    
    cur.execute(f'INSERT INTO album_db (album_name, verified) VALUES ("{album_name}",0)')
    con.commit()
    
    print("New Album Request Sent For : " + album_name)

def get():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM album_db')
    return (cur.fetchall())

def get_by_creator(creator):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM album_db WHERE creator = "{creator}"')
    return (cur.fetchall())

def approve(album_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'UPDATE album_db SET verified = 1 WHERE id = {album_id}')
    con.commit()

def find(album):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM album_db WHERE id = {album}')
    return (cur.fetchone())

def findsongs(album):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM song_db WHERE album_id = {album}')
    return (cur.fetchall())

def count():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From album_db WHERE verified = 1')
    return (cur.fetchone()[0])

def count_by_username(creatorname):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From album_db WHERE creator = "{creatorname}"')
    return (cur.fetchone()[0])

def search(keyword):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f"SELECT * FROM album_db WHERE album_name LIKE ?", ('%' + keyword + '%',))
    return (cur.fetchall())