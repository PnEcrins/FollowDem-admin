from flask import Blueprint, jsonify

from api import animals, devices

api = Blueprint('api', __name__)

def init_app(app):
    app.register_blueprint(animals.animals)
    app.register_blueprint(devices.devices)

