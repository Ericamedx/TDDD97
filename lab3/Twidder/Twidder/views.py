# This file shall contain all the server side remote procedures, implemented using Python and Flask.
import json
import Twidder.database_helper
import math
from random import randint
import random
from flask import Flask, escape, request
#from geventwebsocket.handler import WebSocketHandler
#from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from flask import render_template
#import database_helper
from Twidder import database_helper
#from Twidder import app

app = Flask('Twidder')
X = 5
token = ""
activesockets = dict()

#steg 0 - hello world kolla mot postman?
#steg 0 - hello world kolla mot postman
#1. Use the URL when the used method is GET.
#2. Use JSON when the used method is POST or PUT.
#3. Always use HTTP headers for sending the token.
#You can use the Authorization header for receiving the token.

#start sqlite3 database.db < schema.sql in cmd
#setup python -m flask run with server.py in cmd
#now try different calls in postman/telnet
#if ___name___ == '___main___':
    #http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    #http_server.serve_forever()
#@app.before_request
def beforeRequest():
    database_helper.connect();
@app.teardown_request
def teardownRequest(exception):
    database_helper.closeconnection()
@app.route('/')
def root():
    return app.send_static_file('client.html')
    #return render_template('client.html')
    #name = request.args.get("name", "world")
    #return f'Hello, {escape(name)}!'

def gettoken():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 36):
        token += letters[randint(0,len(letters) - 1)]

    return token
@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        object = ws.receive()
        message = json.loads(object)

        user = database_helper.getSignedinUsertokenByEmail(message['email'])
        if not user:
            jsonobj = json.dumps({"message" : "no such email", "success" : False})
            ws.send(jsonobj)
            #return ''
        try:
            if message['email'] in activesockets:
                print (message['email'] + ' has a socket')
                #jsonobj = json.dumps({"message" : "user already logged in", "success" : False})
                print ('Socket saved with ' + message['email'])
            activesockets[message['email']] = ws

            while True:
                    object = ws.receive()
                    if object == None:
                        activesockets.pop(message['email'], None)
                        ws.close
                        return ''
                        #print("Socket closed for " + data['email'])
        except WebSocketError:
            print ('Web socket connection error ')
            sockets.pop(message['email'], None)
            #for emails in activesockets.keys():
                #if emails == ws:
                    #del activesockets[emails]
                    #break

            #message = ws.wait()
            #ws.send(message)
    return ''
@app.route('/sign_in', methods = ["POST"])
def sign_in():
    #logga in användare
    email = request.form['email'] #eller username
    password = request.form['password']
    token = gettoken()

    result = database_helper.getUserDataByEmail(email)
    if result:
        res2 = database_helper.getSignedinUsertokenByEmail(email)
        if res2:

            database_helper.deleteSignedInUserbyEmail(email)
            # returnera token och succes = true
            if email in activesockets:
                    try:
                        ws = activesockets[email]
                        ws.send(json.dumps({'success' : False, 'message' : 'Session expired'}))
                    except WebSocketError:
                        print ("Sign in web socket error")
                        sockets.pop(email, None)

    result = database_helper.add_signeduser(email, password, token)
    if result:
        jsonobj = json.dumps({"message" : "signed in", "success" : True, "token" : token})
        #connectwithsocket();
        return jsonobj
    else:
        jsonobj = json.dumps({"message" : "wrong password or email", "success" : False, "token" : 0})
        return jsonobj
        # returnera att det är fel namn samt succes = false
@app.route('/sign_up', methods = ["POST"])
def sign_up():
     signupdata = {};
     signupdata['email'] = request.form['email']
     signupdata['password'] = request.form['password']
     signupdata['fname'] = request.form['firstname']
     signupdata['sname'] = request.form['familyname']
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
         if (len(password) >= X):
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
    #token = request.headers['token']
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

@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token():
    #token = request.headers.get['Authorization']
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
    #token = request.form['Authorization']
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
        jsonobj = json.dumps({"message" : "Authorization failed", "success" : True, "posts" : ""})
    else:
        res = database_helper.getUserMessagesByEmail(restoken)
        if(res is not None):
            jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "posts" : res})
        else:
            jsonobj = json.dumps({"message" : "no posts yet", "success" : False, "posts" : ""})

    return jsonobj
@app.route('/get_user_messages_by_email/<email>', methods = ['GET'])
def get_user_messages_by_email(email):
    token = request.headers['Authorization']
    #check if token and user exist
    restoken = database_helper.getUserEmailByToken(token)
    if(restoken is None):
        jsonobj = json.dumps({"message" : "Authorization failed", "success" : False, "posts" : ""})
    else:
        #email = request.form['email']
        res = database_helper.getUserMessagesByEmail(email)
        if(res):
            jsonobj = json.dumps({"message" : "userinfo retrieved", "success" : True, "posts" : res})
        else:
            jsonobj = json.dumps({"message" : "Non existent user", "success" : False, "posts" : ""})

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