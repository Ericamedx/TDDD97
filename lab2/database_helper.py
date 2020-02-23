# This file will contain all the functions that access and control the database and shall contain some SQL
# scripts. This file will be used by the server to access the database. This file shall NOT contain any
# domain functions like signin or signup and shall only contain data-centric functionality like
# find_user(), remove_user(), create_post() and … . E.g. Implementing sign_in() in server.py shall
# involve a call to find_user() implemented in database_helper.py .

import sqlite3

# inspo https://docs.python.org/2/library/sqlite3.html
def connect_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor() # skapa cursor object som sedan används för att kalla på execute()

    # lägg till data genom execute
    c.execute(""" CREATE TABLE IF IT DOES NOT EXIST user(
                Email TEXT PRIMARY KEY,
                Password TEXT,
                Firstname TEXT,
                Familyname TEXT,
                Gender TEXT,
                City TEXT,
                Country TEXT)""")

    # behövs mer sånna tabeller?

    conn.commit() # spara ändringar
    conn.close() # stäng kontakten
    return conn


def find_user(email): # kolla om användaren finns
    #connect_db()
    db = connect_db()
    curs = db.cursor()
    curs.execute(""" SELECT Email, Password FROM user WHERE Email = ? """, (email,))

    if curs.fetchall(): #oklart med denna..
        print('welcome')
    else:
        print('log in failed')

def remove_user():

    pass
def create_post():
    pass
