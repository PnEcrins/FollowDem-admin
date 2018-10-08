from flask import (Blueprint, jsonify, request)
from models import Animal, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

animals = Blueprint('animals', __name__)

@animals.route('/api/animals', methods=['GET'])
def get_animals():
    try:
        animals = Animal.query.\
        order_by(desc(Animal.id)). \
        all()
        return jsonify([ animal.json() for animal in animals ])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@animals.route('/api/animals', methods=['POST'])
def save_animals():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = animals_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animal = Animal(**payload)
    try:
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@animals.route('/api/animals', methods=['PATCH'])
def patch_animals():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = animals_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animal = Animal(**payload)
    try:
        Animal.query.filter_by(id=animal.get('id')).update(animal)
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()
@animals.route('/api/animals', methods=['DELETE'])
def delete_animals():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(Animal).filter(Animal.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def animals_validate_required(animal):
    errors = []
    for attr in ('name', 'birth_year', 'capture_date', 'death_date'):
        if not animal.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'animals',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True
