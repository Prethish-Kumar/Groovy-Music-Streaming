import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def login_user(email,password):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE email = "{email.lower()}"')
    user = cur.fetchone()
    if user:
      user_password = user[3] 
      if hash_password(password) == user_password:
         return True


def getUserName(email):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE email = "{email.lower()}"')
    user = cur.fetchone()

    if user:
      user_name = user[1] 
      return user_name
    
def getRole(email):
    con = sqlite3.connect("groovy.db")

    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE email = "{email.lower()}"')
    user = cur.fetchone()

    if user:
      user_name = user[4] 
      return user_name