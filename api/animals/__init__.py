from flask import (Blueprint, jsonify, request)
from models import Animal, AnimalDevice, db, AnimalAttribute
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
        return jsonify([animal.json() for animal in animals])
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

@animals.route('/api/animals/devices', methods=['POST'])
def save_animal_devices():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = animal_devices_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animalDevice = AnimalDevice(**payload)
    try:
        db.session.add(animalDevice)
        db.session.commit()
        animal = Animal.query.get(animalDevice.animal_id)
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@animals.route('/api/animals/attributes', methods=['POST'])
def save_animal_attributes():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = animal_attributes_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animalAttribute = AnimalAttribute(**payload)
    try:
        db.session.add(animalAttribute)
        db.session.commit()
        animal = Animal.query.get(animalAttribute.animal_id)
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@animals.route('/api/animals/devices', methods=['DELETE'])
def delete_animal_devices():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(AnimalDevice).filter(AnimalDevice.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@animals.route('/api/animals/attributes', methods=['DELETE'])
def delete_animal_attributes():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(AnimalAttribute).filter(AnimalAttribute.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@animals.route('/api/animals/<int:id>', methods=['GET'])
def get_animal_by_id(id=id):
    animal = Animal.query.get(id)
    if animal:
        return jsonify(animal.json())
    else:
        return 'error not found'

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
        id = int(payload['id'])
        del payload['id']
        db.session.query(Animal).filter(Animal.id == id).update(payload)
        db.session.commit()
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

def animal_devices_validate_required(animal):
    errors = []
    for attr in ('start_at', 'end_at', 'animal_id', 'device_id'):
        if not animal.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'animals',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True
def animal_attributes_validate_required(animal):
    errors = []
    for attr in ('value', 'animal_id', 'attribute_id'):
        if not animal.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'animals',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True