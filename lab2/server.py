# This file shall contain all the server side remote procedures, implemented using Python and Flask.
from flask import Flask, escape, request

app = Flask(__name__)

#steg 0 - hello world kolla mot postman?
#steg 0 - hello world kolla mot postman
@app.route('/')
def hello():
    name = request.args.get("name", "world")
    return f'Hello, {escape(name)}!'

@app.route('/sign_in', methods = ["POST"])
def sign_in():
    #logga in användare
    email = request.form['email'] #eller username
    password = request.form['password']
    user_info = database_helper.find_user(email)

    if user_info and user_info["email"] == email and user_info["password"] == password:
        # returnera token och succes = true
    else:
        # returnera att det är fel namn samt succes = false
