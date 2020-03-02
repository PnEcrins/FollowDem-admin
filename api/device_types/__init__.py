from flask import (Blueprint, jsonify, request)
from models import DeviceType, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc
from pypnusershub import routes as fnauth

device_types = Blueprint('device_types', __name__)

@device_types.route('/api/device_types', methods=['GET'])
@fnauth.check_auth(4)
def get_DeviceTypes():
    try:
        device_types = DeviceType.query.\
        order_by(desc(DeviceType.id)). \
        all()
        return jsonify([ DeviceType.json() for DeviceType in device_types ])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400
@device_types.route('/api/device_types/<int:id>', methods=['GET'])
@fnauth.check_auth(4)
def get_device_by_id(id=id):
    try:
        device_type = DeviceType.query.get(id)
        if device_type:
            return jsonify(device_type.json())
        else:
            return 'error not found'
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@device_types.route('/api/device_types', methods=['POST'])
@fnauth.check_auth(4)
def save_DeviceTypes():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = device_types_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    device_type = DeviceType(**payload)
    try:
        db.session.add(device_type)
        db.session.commit()
        return jsonify(device_type.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@device_types.route('/api/device_types', methods=['PATCH'])
@fnauth.check_auth(4)
def patch_DeviceTypes():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = device_types_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    device_type = DeviceType(**payload)
    try:
        id = int(payload['id'])
        del payload['id']
        db.session.query(DeviceType).filter(DeviceType.id == id).update(payload)
        db.session.commit()
        return jsonify(device_type.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@device_types.route('/api/device_types', methods=['DELETE'])
@fnauth.check_auth(4)
def delete_DeviceTypes():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            db.session.query(DeviceType).filter(DeviceType.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def device_types_validate_required(device_type):
    errors = []
    for attr in (['name']):
        if not device_type.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'device_types',
                'column': attr
            })
    name = device_type.get('name').lower()
    name = name.strip()
    device_type_exist = DeviceType.query.filter(DeviceType.name == name).first()
    if device_type_exist and (device_type_exist.json().get('id') != device_type.get('id')): 
          errors.append({
                'name': 'attribute_already_exists', 
                'table': 'device_types',
                'column': 'name'
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True



