# This file will contain all the functions that access and control the database and shall contain some SQL
# scripts. This file will be used by the server to access the database. This file shall NOT contain any
# domain functions like signin or signup and shall only contain data-centric functionality like
# find_user(), remove_user(), create_post() and … . E.g. Implementing sign_in() in server.py shall
# involve a call to find_user() implemented in database_helper.py .

import sqlite3
#from flask import Flask
#from flask import g

#app = Flask(__name__)
conn = sqlite3.connect('database.db')
c = conn.cursor()
databaseConnection = None
# inspo https://docs.python.org/2/library/sqlite3.html
def connect_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor() # skapa cursor object som sedan används för att kalla på execute()

     #lägg till data genom execute
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                email VARCHAR(200) PRIMARY KEY,
                password VARCHAR(60) NOT NULL,
                firstName VARCHAR(200) NOT NULL,
                lastName VARCHAR(200) NOT NULL,
                gender VARCHAR(10) NOT NULL,
                city VARCHAR(200) NOT NULL,
                country VARCHAR(200) NOT NULL);
                """)
    c.execute("""CREATE TABLE IF NOT EXISTS signedInUsers(
                token VARCHAR(36) PRIMARY KEY,
                email VARCHAR(200) NOT NULL,
                FOREIGN KEY (email) REFERENCES users(email));
                """)
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
                messageId INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                datePosted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                browsedemail VARCHAR(200) NOT NULL,
                writer VARCHAR(200) NOT NULL,
                FOREIGN KEY (browsedemail) REFERENCES users(email),
                FOREIGN KEY (writer) REFERENCES users(email));
                """)

                #DROP TABLE IF EXISTS users;
                #DROP TABLE IF EXISTS signedInUsers;
                #DROP TABLE IF EXISTS messages;
    # behövs mer sånna tabeller?

    conn.commit() # spara ändringar
    #conn.close() # stäng kontakten
    return conn

def add_signeduser(email, password, token):
    #realpassword = query_db('select password from users where email = ?', (email,))
    #realpassword = 'test'
    #should we check if the user is already in the signedinusers table?
    databaseConnection = connect_db()
    cursor = databaseConnection.cursor()
    cursor.execute('select password from users where email = ?', (email,))
    realpassword = cursor.fetchone()
    cursor.execute('select token from signedInUsers where email = ?', (email,))
    signedinusertoken = cursor.fetchone()
    if(signedinusertoken):
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
	#databaseConnection = sqlite3.connect('database.db')
    databaseConnection = connect_db()
    #databaseConnection = sqlite3.connect('database.db')
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    databaseConnection.commit()
    cursor.close()
    databaseConnection.close()
    return True

def query_db_one(query, args=()):
    #databaseConnection = sqlite3.connect('database.db')
    databaseConnection = connect_db()
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchone()
    cursor.close()
    return result
def query_db_all(query, args=()):
    databaseConnection = connect_db()
    cursor = databaseConnection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return result
    #return None
def getUserDataByToken(token): # kolla om användaren finns
    #connect_db()
    #connect()
    email = getUserEmailByToken(token)
    return getUserDataByEmail(email)

def getUserDataByEmail(email):
    return query_db_one('select email, password, firstName, lastName, gender, city, country from users where email = ?', (email,))
def add_user(email, password, firstName, lastName, country, city, gender):
    return query_db('insert into users values (?, ?, ?, ?, ?, ?, ?)',(email, password, firstName, lastName, gender, city, country))

def getUserMessagesByEmail(email):
    return query_db_all('select datePosted, writer, message from messages where browsedemail = ?', (email,))
def getUserMessagesByToken(token):
    return query_db_all('select * from messages where browsedemail = ?', (token,))
def getSignedinUsertokenByEmail(email):
    data = query_db_one('select token, email from signedInUsers where email = ?', (email,))
    if data:
        return data[0]
    else:
        return 0
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
def deleteSignedInUserbyEmail(email):
    return query_db('delete from signedInUsers where email = ?', (email,))

def updateUserPassword(email, password):
    return query_db('update users set password = ? where email = ?', (password, email))
