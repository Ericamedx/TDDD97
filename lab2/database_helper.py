# This file will contain all the functions that access and control the database and shall contain some SQL
# scripts. This file will be used by the server to access the database. This file shall NOT contain any
# domain functions like signin or signup and shall only contain data-centric functionality like
# find_user(), remove_user(), create_post() and … . E.g. Implementing sign_in() in server.py shall
# involve a call to find_user() implemented in database_helper.py .

import sqlite3
from flask import Flask
from flask import g

app = Flask(__name__)
conn = sqlite3.connect('database.db')
c = conn.cursor()
databaseConnection = None
# inspo https://docs.python.org/2/library/sqlite3.html
def connect_db():
    #conn = sqlite3.connect('database.db')
    #c = conn.cursor() # skapa cursor object som sedan används för att kalla på execute()

    # lägg till data genom execute
    #c.execute(""" CREATE TABLE IF IT DOES NOT EXIST user(
                #Email TEXT PRIMARY KEY,
                #Password TEXT,
                #Firstname TEXT,
                #Familyname TEXT,
                #Gender TEXT,
                #City TEXT,
                #Country TEXT)""")

    # behövs mer sånna tabeller?

    conn.commit() # spara ändringar
    conn.close() # stäng kontakten
    return conn

def add_signeduser(email, password, token):
    #realpassword = query_db('select password from users where email = ?', (email,))
    #realpassword = 'test'
    cursor = databaseConnection.cursor()
    cursor.execute('select password from users where email = ?', (email,))
    realpassword = cursor.fetchone()

    if (realpassword[0] == password):
        cursor.execute('insert into signedInUsers values (?,?)', (token, email,))
        cursor.close()
        return True
    else:
        cursor.close()
        return False
def find_user(email): # kolla om användaren finns
    #connect_db()
    db = g._database = sqlite3.connect('database.db')
    curs = db.cursor()
    curs.execute(""" SELECT Email, Password FROM users WHERE Email = ? """, (email,))

    res = curs.fetchall()
    curs.close()
    return res;
    #if curs.fetchall(): #oklart med denna..
    #    print('welcome')
    #else:
    #    print('log in failed')

def add_user(email, password, firstName, lastName, country, city, gender):
    return query_db('insert into users values (?, ?, ?, ?, ?, ?, ?)',(email, password, firstName, lastName, gender, city, country))

def connect():
    global databaseConnection
    databaseConnection = sqlite3.connect('database.db')

def query_db(query, args=()):
	#db= sqlite3.connect('database.db')
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    databaseConnection.commit()
    cursor.close()
    return True
    #print rv
	#cur.close()
	#db.commit()
    #return rv
	#return (rv[0] if rv else None) if one else rv

def remove_user():

    pass
def create_post():
    pass
