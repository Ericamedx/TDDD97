# This file shall contain all the server side remote procedures, implemented using Python and Flask.
from flask import Flask, escape, request
import json
import database_helper
import math
from random import randint
import random
app = Flask(__name__)
X = 5
token = ""

#steg 0 - hello world kolla mot postman?
#steg 0 - hello world kolla mot postman
#1. Use the URL when the used method is GET.
#2. Use JSON when the used method is POST or PUT.
#3. Always use HTTP headers for sending the token.
#You can use the Authorization header for receiving the token.

#start sqlite3 database.db < schema.sql in cmd
#setup python -m flask run with server.py in cmd
#now try different calls in postman/telnet
@app.before_request
def beforeRequest():
    database_helper.connect();
@app.teardown_request
def teardownRequest(exception):
    database_helper.closeconnection()
@app.route('/')
def hello():
    name = request.args.get("name", "world")
    return f'Hello, {escape(name)}!'

def gettoken():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 36):
        token += letters[randint(0,len(letters) - 1)]

    return token
@app.route('/sign_in', methods = ["POST"])
def sign_in():
    #logga in användare
    email = request.form['email'] #eller username
    password = request.form['password']
    token = gettoken()
    result = database_helper.add_signeduser(email, password, token)
    if result:
        # returnera token och succes = true
        jsonobj = json.dumps({"message" : "signed in", "success" : True, "token" : token})
        return jsonobj
    else:
        jsonobj = json.dumps({"message" : "something went wrong", "success" : False, "token" : 0})
        return jsonobj
        # returnera att det är fel namn samt succes = false
@app.route('/sign_up', methods = ['GET'])
def sign_up():
     signupdata = {};
     signupdata['email'] = request.form['email']
     signupdata['password'] = request.form['password']
     signupdata['fname'] = request.form['firstname']
     signupdata['sname'] = request.form['surname']
     signupdata['country'] = request.form['country']
     signupdata['city'] = request.form['city']
     signupdata['gender'] = request.form['gender']
     email = signupdata['email']
     password = signupdata['password']
     fname = signupdata['fname']
     sname = signupdata['sname']
     country = signupdata['country']
     city = signupdata['city']
     gender = signupdata['gender']
     res = database_helper.getUserDataByEmail(email)
     if res is not None:
         jsonobj = json.dumps({"message" : "email already exists", "success" : False})
         return jsonobj

     if(email and password and fname and sname and country and city and gender):
         if (len(password) > X):
              database_helper.add_user(email, password, fname, sname, country, city, gender);
              jsonobj = json.dumps({"message" : "added user", "success" : True, "email" : email, "password" : password, "firstname" : fname, "sname" : sname, "country" : country, "city": city, "gender": gender})
              return jsonobj
         else:
             jsonobj = json.dumps({"message" : "no, 2 short password", "success" : False})
             return jsonobj
     else:
         jsonobj = json.dumps({"message" : "no, some field is empty", "success" : False})
         return jsonobj

@app.route('/sign_out', methods = ['POST'])
  #remove token? but its already been done at clientside.
def sign_out():
    token = request.headers['Authorization']
    #token = request.form['token']
    result = database_helper.removesigneduser(token)
    if result is not None:
        jsonobj = json.dumps({"message" : "logged out", "success" : True})
    else:
        jsonobj = json.dumps({"message" : "not signed out" , "success" : False})
     #token = 0
     # jsonobj = json.dumps({"true" : "no", "success" : False})
      #return jsonobj
    #jsonobj = json.dumps({"true" : "no", "success" : False})
    return jsonobj
@app.route('/Change_password', methods = ['POST'])
def changepassword():
    token = request.headers['Authorization']
    oldPassword = request.form['oldPassword']
    newPassword = request.form['newPassword']
    email = database_helper.getUserEmailByToken(token)
    serverpass = database_helper.getUserPasswordByEmail(email)
    if(serverpass == oldPassword):
        res = database_helper.updateUserPassword(email, newPassword)


        jsonobj = json.dumps({"message" : "changed the password", "success" : res})
        return jsonobj
    else:
        jsonobj = json.dumps({"message" : "wrong password", "success" : False})
        return jsonobj
    #return "hej"

@app.route('/get_user_data_by_token', methods = ['POST'])
def get_user_data_by_token():
    token = request.headers['Authorization']
    res = database_helper.getUserDataByToken(token)
    if(res is not None):
        jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "userinfo" : res})
    else:
        jsonobj = json.dumps({"message" : "no data for that email", "success" : False})

    return jsonobj

@app.route('/get_user_data_by_email/<email>', methods = ['GET'])
def get_user_data_by_email(email):
    #email = request.form['email']
    token = request.headers['Authorization']
    #check if token and user exist
    restoken = database_helper.getUserEmailByToken(token)
    if(restoken is None):
        jsonobj = json.dumps({"message" : "Authorization failed", "success" : True})
    else:
        res = database_helper.getUserDataByEmail(email)
        if(res is not None):
            jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "userinfo" : res})
        else:
            jsonobj = json.dumps({"message" : "no data for that email", "success" : False})

    return jsonobj

@app.route('/Get_user_messages_by_token/', methods = ['GET'])
def Get_user_messages_by_token():
    token = request.headers['Authorization']
    #check if token and user exist
    restoken = database_helper.getUserEmailByToken(token)
    if(restoken is None):
        jsonobj = json.dumps({"message" : "Authorization failed", "success" : True})
    else:
        res = database_helper.getUserMessagesByToken(token)
        if(res is not None):
            jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "posts" : res})
        else:
            jsonobj = json.dumps({"message" : "no posts yet", "success" : False})

    return jsonobj
@app.route('/get_user_messages_by_email/<email>', methods = ['GET'])
def get_user_messages_by_email(email):
    token = request.headers['Authorization']
    #check if token and user exist
    restoken = database_helper.getUserEmailByToken(token)
    if(restoken is None):
        jsonobj = json.dumps({"message" : "Authorization failed", "success" : True})
    else:
        #email = request.form['email']
        res = database_helper.getUserMessagesByEmail(email)
        if(res):
            jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "posts" : res})
        else:
            jsonobj = json.dumps({"message" : "Non existent user", "success" : False})

    return jsonobj
@app.route('/post_message', methods = ['POST'])
def post_message():
    #needs to check if user exist, both the poster and the brosedemail, and needs token
    token = request.headers['Authorization']
    writerEmail = database_helper.getUserEmailByToken(token)
    message = request.form['message']
    browsedemail = request.form['email']
    res2 = database_helper.getUserDataByEmail(browsedemail)

    res = None
    if writerEmail is not None and res2 is not None:
        res = database_helper.insertMessage(writerEmail, browsedemail, message)
    if(res is not None):
        jsonobj = json.dumps({"message" : "you posted", "success" : True})
    else:
        jsonobj = json.dumps({"message" : "Either not logged in or none existend browsed user", "success" : False})

    return jsonobj
