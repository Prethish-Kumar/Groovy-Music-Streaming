import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def new_creator(creator_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f"""UPDATE users
                    SET verified = 0
                    WHERE id = "{creator_id}";"""
                )
    
    con.commit()


def get_id(creator_username):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f"""SELECT id from users WHERE username = '{creator_username}' """)
    
    return cur.fetchone()


def approve(creator_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'UPDATE users SET verified = 1,role = 2 WHERE id = {creator_id}')
    con.commit()

def usercount():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From users WHERE role = 1')
    return (cur.fetchone()[0])

def creatorcount():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From users WHERE role = 2')
    return (cur.fetchone()[0])

def get():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM users')
    return (cur.fetchall())