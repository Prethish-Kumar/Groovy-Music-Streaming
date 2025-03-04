import sqlite3

def search(keyword):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE role = 2 AND username LIKE '%{keyword}%';')
    return (cur.fetchone())