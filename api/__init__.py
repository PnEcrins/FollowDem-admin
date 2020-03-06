from flask import Blueprint, jsonify

from api import animals, devices, device_types, attributes

api = Blueprint('api', __name__)
from pypnusershub.routes import routes


def init_app(app):
    app.register_blueprint(routes, url_prefix='/auth')
    app.register_blueprint(animals.animals)
    app.register_blueprint(devices.devices)
    app.register_blueprint(device_types.device_types)
    app.register_blueprint(attributes.attributes)



