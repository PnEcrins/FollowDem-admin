from flask import (Blueprint, jsonify, request)
from models import DeviceType, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

device_types = Blueprint('device_types', __name__)

@device_types.route('/api/device_types', methods=['GET'])
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
def delete_DeviceTypes():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(DeviceType).filter(DeviceType.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def device_types_validate_required(DeviceType):
    errors = []
    for attr in (['name']):
        if not DeviceType.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'device_types',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True
