# This file shall contain all the server side remote procedures, implemented using Python and Flask.
from flask import Flask, escape, request
import json
import database_helper
app = Flask(__name__)

#steg 0 - hello world kolla mot postman?
#steg 0 - hello world kolla mot postman
@app.route('/')
def hello():
    name = request.args.get("name", "world")
    return f'Hello, {escape(name)}!'

@app.route('/sign_in', methods = ["POST" , "GET"])
def sign_in():
    #logga in användare
    email = request.form['email'] #eller username
    password = request.form['password']
    user_info = database_helper.find_user(email)

    if user_info and user_info["email"] == email and user_info["password"] == password:
        # returnera token och succes = true
        jsonobj = json.dumps({"true" : "yes", "success" : True, "token" : 1})
        return jsonobj
    else:
        pass
        # returnera att det är fel namn samt succes = false
@app.route('/sign_up', methods = ['GET'])
def sign_up():
     email = request.form['email']
     password = request.form['password']
     fname = request.form['firstname']
     sname = request.form['surname']
     country = request.form['country']
     city = request.form['city']
     gender = request.form['gender']

     if(email and password and fname and sname and country and city and gender and (len(password) > 5)):
         #if (len(password) < 5):
             jsonobj = json.dumps({"true" : "yes", "success" : True, "email" : email, "password" : password, "firstname" : fname, "sname" : sname, "country" : country, "city": city, "gender": gender})
             return jsonobj
     else:
         jsonobj = json.dumps({"true" : "no", "success" : False})
         return jsonobj

@app.route('/sign_out', methods = ['GET'])
  #remove token? but its already been done at clientside.
def sign_out():
     #token = 0
     # jsonobj = json.dumps({"true" : "no", "success" : False})
      #return jsonobj
    jsonobj = json.dumps({"true" : "no", "success" : False})
    return jsonobj
@app.route('/Change_password', methods = ['POST'])
def changepassword():
    token = request.form['token']
    oldPassword = request.form['oldPassword']
    newPassword = request.form['newPassword']

    #database_helper.getpassword etc..
    return "hej"

#@app.route('/get_user_data_by_token', methods = ['GET'])

#@app.route('/get_user_data_by_email', methods = ['GET'])

#@app.route('/Get_user_messages_by_token', methods = ['GET'])

#@app.route('/get_user_messages_by_email', methods = ['GET'])

#@app.route('/post_message', methods = ['POST'])
