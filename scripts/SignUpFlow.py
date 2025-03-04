import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def new_user(username,email,password):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role INTEGER,
                verified INTEGER
                )""")
    cur.execute(f'INSERT INTO users (username, email, password, role, verified) VALUES ("{username}","{email.lower()}","{hash_password(password)}",1,1)')
    
    con.commit()
    
    res = cur.execute("SELECT * FROM users")
    print(res.fetchall())

