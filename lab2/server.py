# This file shall contain all the server side remote procedures, implemented using Python and Flask.
from flask import Flask, escape, request

app = Flask(__name__)

#steg 0 - hello world kolla mot postman?
@app.route('/')
def hello():
    name = request.args.get("name", "world")
    return f'Hello, {escape(name)}!'
