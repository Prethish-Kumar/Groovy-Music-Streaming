import sqlite3
import hashlib

from flask import redirect


def add(creator,song_name,mp3_path,lyrics_path):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS song_db(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator TEXT NOT NULL,
                song_name TEXT NOT NULL,
                mp3_path varchar(10) NOT NULL,
                lyrics_path varchar(10) NOT NULL,
                verified INTEGER,
                album_id INTEGER
                )""")
    
    cur.execute(f'INSERT INTO song_db (creator,song_name, mp3_path, lyrics_path, verified,album_id) VALUES ("{creator}","{song_name}","{mp3_path}","{lyrics_path}",0,0)')
    
    con.commit()
    
    print("New Song Request Sent For : " + song_name)

def get():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM song_db')
    return (cur.fetchall())

def get_by_creator(creator):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM song_db WHERE creator = "{creator}"')
    return (cur.fetchall())

def approve(song_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'UPDATE song_db SET verified = 1 WHERE id = {song_id}')
    con.commit()

def find(song_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM song_db WHERE id = {song_id}')
    return (cur.fetchone())

def count():
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From song_db WHERE verified = 1')
    return (cur.fetchone()[0])

def count_by_username(creatorname):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT COUNT(*) From song_db WHERE creator = "{creatorname}"')
    return (cur.fetchone()[0])

def addtoalbum(song_id,album_id):
    con = sqlite3.connect("groovy.db")
    cur = con.cursor()
    cur.execute(f"""UPDATE song_db
                  SET album_id = {album_id}
                  WHERE id= {song_id};""")
    con.commit()
    return redirect("/creator")

def search(keyword):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f"SELECT * FROM song_db WHERE song_name LIKE ?", ('%' + keyword + '%',))
    return (cur.fetchall())