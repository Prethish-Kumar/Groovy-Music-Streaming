import sqlite3

def add(creator,name):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS playlists(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator TEXT NOT NULL,
                name TEXT NOT NULL
                )""")
    
    cur.execute(f'INSERT INTO playlists (creator,name) VALUES ("{creator}","{name}")')
    
    con.commit()

def get_by_creator(creator):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM playlists WHERE creator = "{creator}"')
    return (cur.fetchall())

def get_by_id(playlist_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM playlists WHERE id = {playlist_id}')
    return (cur.fetchone())

def addtoplaylist(song_id,playlist_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'INSERT INTO playlist_songs (playlist_id, song_id) VALUES ({playlist_id}, {song_id});')
    con.commit() 

def getSongsForPlaylist(playlist_id):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f"""SELECT
                song_id
                FROM
                    playlists
                JOIN
                    playlist_songs ON playlists.id = playlist_songs.playlist_id
                WHERE 
                playlists.id = {playlist_id}	
                """)
    songs = [item[0] for item in cur.fetchall()]
    if len(songs) > 1:
        songs_tuple = tuple(songs)
        cur.execute(f'SELECT * From song_db WHERE id IN {songs_tuple}')
        return (cur.fetchall())
    if len(songs) == 1:
        songs_tuple = songs[0]
        cur.execute(f'SELECT * From song_db WHERE id IN ({songs_tuple})')
        return (cur.fetchall())
    
    if len(songs) == 0:
        return ([])
