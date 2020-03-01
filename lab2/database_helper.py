# This file will contain all the functions that access and control the database and shall contain some SQL
# scripts. This file will be used by the server to access the database. This file shall NOT contain any
# domain functions like signin or signup and shall only contain data-centric functionality like
# find_user(), remove_user(), create_post() and … . E.g. Implementing sign_in() in server.py shall
# involve a call to find_user() implemented in database_helper.py .

import sqlite3
from flask import Flask
from flask import g

#app = Flask(__name__)
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
    #should we check if the user is already in the signedinusers table?
    cursor = databaseConnection.cursor()
    cursor.execute('select password from users where email = ?', (email,))
    realpassword = cursor.fetchone()
    cursor.execute('select token from signedInUsers where email = ?', (email,))
    signedinusertoken = cursor.fetchone()
    if(signedinusertoken == token):
        return False
    if(realpassword is None):
        return False
    if (realpassword[0] == password):
        query_db('insert into signedInUsers values (?,?)', (token, email,))
        #cursor.close()
        return True
    else:
        cursor.close()
        return False

def removesigneduser(token):
    #not sure if user really gets deleted.
    return query_db('DELETE FROM signedInUsers WHERE token = ?', (token,))
    #cursor = databaseConnection.cursor()
    #cursor.execute('remove signedInUsers values (?,?) where token =?', (token,))
    #res = cursor.fetchall()
    #if(res is None):
    #        return False
    #    else:
    #        return True

def connect():
    global databaseConnection
    databaseConnection = sqlite3.connect('database.db')
def closeconnection():
    if (databaseConnection is not None):
        databaseConnection.close()
def query_db(query, args=()):
	#db= sqlite3.connect('database.db')
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    databaseConnection.commit()
    cursor.close()
    return True

def query_db_one(query, args=()):
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchone()
    cursor.close()
    return result
def query_db_all(query, args=()):
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return result
    #return None
def getUserDataByToken(token): # kolla om användaren finns
    #connect_db()
    email = getUserEmailByToken(token)
    return getUserDataByEmail(email)
    
def getUserDataByEmail(email):
    return query_db_one('select * from users where email = ?', (email,))
def add_user(email, password, firstName, lastName, country, city, gender):
    return query_db('insert into users values (?, ?, ?, ?, ?, ?, ?)',(email, password, firstName, lastName, gender, city, country))

def getUserMessagesByEmail(email):
    return query_db_all('select * from messages where browsedemail = ?', (email,))
def getUserMessagesByToken(token):
    return query_db_all('select * from messages where browsedemail = ?', (email,))
def getUserEmailByToken(token):
    email = query_db_one('select email from signedInUsers where token = ?', (token,))
    if email is not None:
        return email[0]
    else:
        return None

def getUserPasswordByEmail(email):
    password = query_db_one('select password from users where email = ?', (email,))
    if password is not None:
        return password[0]
    else:
        return None

def insertMessage(writerEmail, email, message):
    return query_db('insert into messages (message, browsedemail, writer) values (?, ?, ?)', (message, email, writerEmail))

def deleteSignedInUser(token):
    return query_db('delete from signedInUsers where token = ?', (token,))

def updateUserPassword(email, password):
    return query_db('update users set password = ? where email = ?', (password, email))
def remove_user():

    pass
def create_post():
    pass
