from flask import (Blueprint, jsonify, request)
from models import Animal, AnimalDevice, db, AnimalAttribute, Device
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc, or_
#Import de la librairie
from pypnusershub import routes as fnauth

animals = Blueprint('animals', __name__)

@animals.route('/api/animals', methods=['GET'])
@fnauth.check_auth(4)
def get_animals():
    try:
        key = request.args.get("key")
        animals = []
        if key:
            animals = Animal.query. \
                filter(or_(Animal.name.like("%" + key + "%"))). \
                order_by(desc(Animal.id)). \
                all()
        else:
            animals = Animal.query.\
            order_by(desc(Animal.id)). \
            all()
        return jsonify([animal.json() for animal in animals])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@animals.route('/api/animals', methods=['POST'])
@fnauth.check_auth(4)
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
@fnauth.check_auth(4)
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
    device = Device.query.get(payload.get('device_id'))
    snDs = db.session.query(
        Device,
        AnimalDevice
    ).filter(
        Device.device_type_id == device.device_type_id
    ).filter(
        Device.id == AnimalDevice.device_id
    ).filter(
        animalDevice.start_at >= AnimalDevice.start_at
    ).filter(
        animalDevice.end_at <= AnimalDevice.end_at
    ).all()
    if(snDs):
        return jsonify(error={'name': 'invalid_period',
                              'errors': 'animal can have only one device active on same type'}), 400
    try:
        if 'id' in payload:
            id = int(payload['id'])
            del payload['id']
            db.session.query(AnimalDevice).filter(AnimalDevice.id == id).update(payload)
        else:
            db.session.add(animalDevice)
            db.session.commit()
        animal = Animal.query.get(animalDevice.animal_id)
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@animals.route('/api/animals/attributes', methods=['POST'])
@fnauth.check_auth(4)
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
        if 'id' in payload:
            id = int(payload['id'])
            del payload['id']
            db.session.query(AnimalAttribute).filter(AnimalAttribute.id == id).update(payload)
        else:
            db.session.add(animalAttribute)
            db.session.commit()
        animal = Animal.query.get(animalAttribute.animal_id)
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@animals.route('/api/animals/devices', methods=['DELETE'])
@fnauth.check_auth(4)
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
@fnauth.check_auth(4)
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
@fnauth.check_auth(4)
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
@fnauth.check_auth(4)
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