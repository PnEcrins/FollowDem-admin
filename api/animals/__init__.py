from flask import (Blueprint, jsonify, request)
from models import Animal, AnimalDevice, db, AnimalAttribute, Device
import traceback
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc, or_
from datetime import datetime
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
                filter(or_(Animal.name.ilike("%" + key + "%"))). \
                order_by(desc(Animal.id_animal)). \
                all()
        else:
            animals = Animal.query.\
                order_by(desc(Animal.id_animal)). \
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
        animal_to_add = payload.get('animal')
        devices_to_add = payload.get('devices')
        attributes_to_add = payload.get('attributes')
    except Exception:
        return jsonify(error='Invalid JSON.')
    validation = animals_validate_required(animal_to_add)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animal = Animal(**animal_to_add)
    if devices_to_add:
        list_devices = []
        for item in devices_to_add:
            tmp = AnimalDevice(**item)
            list_devices.append(tmp)
        animal.animal_devices = list_devices
    if attributes_to_add:
        list_attributes = []
        for item in attributes_to_add:
            tmp = AnimalAttribute(**item)
            list_attributes.append(tmp)
        animal.animal_attributes = list_attributes
    try:
        db.session.add(animal)
        db.session.commit()
        return jsonify(animal.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()


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
        animal_to_update = payload.get('animal')
        attributes = payload.get('attributes')
        devices = payload.get('devices')
        id = int(animal_to_update['id_animal'])
    except Exception:
        return jsonify(error='Invalid JSON.')
    validation = animals_validate_required(animal_to_update)
    del animal_to_update['id_animal']
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    animal = Animal(**animal_to_update)

    try:
        db.session.query(Animal).filter(
            Animal.id_animal == id).update(animal_to_update)
        db.session.query(AnimalAttribute).filter(
            AnimalAttribute.id_animal == id).delete()
        db.session.query(AnimalDevice).filter(
            AnimalDevice.id_animal == id).delete()
        if attributes:
            for attribute in attributes:
                attribute['id_animal'] = id
                db.session.add(AnimalAttribute(**attribute))

        if devices:
            for device in devices:
                device['id_animal'] = id
                db.session.add(AnimalDevice(**device))
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
            db.session.query(Animal).filter(Animal.id_animal == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def animals_validate_required(animal):
    errors = []
    for attr in ('name', 'birth_year', 'capture_date'):
        if not animal.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'animals',
                'column': attr
            })
        # name must be unique
        name = animal.get('name').lower()
        name = name.strip()
        animal_exist = Animal.query.filter(Animal.name == name).first()
        if (animal_exist and (animal_exist.json().get('id') != animal.get('id'))):
            errors.append({
                'name': 'attribute_already_exists',
                'table': 'animals',
                'column': 'name'
            })
    if len(errors) >= 0:
        return {'errors': errors}
    return True


@animals.route('/api/animals/device_available', methods=['GET'])
@fnauth.check_auth(4)
def check_devices_available(id=id):
    try:
        id_device = int(request.args.get('deviceId'))
        id_animal = int(request.args.get('animalId'))
    except Exception:
        return jsonify(error='Invalid JSON.')
    try:
        now = datetime.now()
        device_exist = AnimalDevice.query.filter(
            AnimalDevice.id_device == id_device,
            AnimalDevice.id_animal != id_animal,
            ).first()     
        if (device_exist and (not device_exist.json().get('date_end') or device_exist.json().get('date_end') > now)):
            return jsonify([id_device]), 200
        return jsonify([]), 200
    except Exception:
        return jsonify(error='server error'), 500
