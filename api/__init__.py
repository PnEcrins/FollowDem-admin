from flask import Blueprint, jsonify

from api import animals

api = Blueprint('api', __name__)

def init_app(app):
    app.register_blueprint(animals.animals)

