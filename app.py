#!/usr/bin/python3

import os
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def hello():
    return 'hello followDem-server !'