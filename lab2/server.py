# This file shall contain all the server side remote procedures, implemented using Python and Flask.
from flask import Flask, escape, request
import json
import database_helper
app = Flask(__name__)
X = 5;

#steg 0 - hello world kolla mot postman?
#steg 0 - hello world kolla mot postman
#1. Use the URL when the used method is GET.
#2. Use JSON when the used method is POST or PUT.
#3. Always use HTTP headers for sending the token.
#You can use the Authorization header for receiving the token.
@app.before_request
def beforeRequest():
    database_helper.connect();

@app.route('/')
def hello():
    name = request.args.get("name", "world")
    return f'Hello, {escape(name)}!'

@app.route('/sign_in', methods = ["POST" , "GET"])
def sign_in():
    #logga in användare
    email = request.form['email'] #eller username
    password = request.form['password']
    token = 1
    result = database_helper.add_signeduser(email, password, token)

    if result:
        # returnera token och succes = true
        jsonobj = json.dumps({"true" : "yes", "success" : True, "token" : 1})
        return jsonobj
    else:
        jsonobj = json.dumps({"true" : "no", "success" : False, "token" : 0})
        return jsonobj
        pass
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

     if(email and password and fname and sname and country and city and gender and (len(password) > 5)):
         if (len(password) > X):
              database_helper.add_user(email, password, fname, sname, country, city, gender);
              jsonobj = json.dumps({"true" : "yes", "success" : True, "email" : email, "password" : password, "firstname" : fname, "sname" : sname, "country" : country, "city": city, "gender": gender})
              return jsonobj
         else:
             jsonobj = json.dumps({"true" : "no", "success" : False})
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
