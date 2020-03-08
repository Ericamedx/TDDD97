from flask import Flask, request
from gevent.pywsgi import WSGIServer
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import Twidder.views
from Twidder.views import app

if __name__ == "__main__":
    #app.debug = True
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
    app.run()
