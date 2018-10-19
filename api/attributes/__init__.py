from flask import (Blueprint, jsonify, request)
from models import Attribute, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

attributes = Blueprint('attributes', __name__)

@attributes.route('/api/attributes', methods=['GET'])
def get_attributes():
    try:
        attributes = Attribute.query.\
        order_by(desc(Attribute.id)). \
        all()
        return jsonify([ Attribute.json() for Attribute in attributes ])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@attributes.route('/api/attributes', methods=['POST'])
def save_attributes():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = attributes_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    attribute = Attribute(**payload)
    try:
        db.session.add(attribute)
        db.session.commit()
        return jsonify(attribute.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@attributes.route('/api/attributes', methods=['PATCH'])
def patch_attributes():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = attributes_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    attribute = Attribute(**payload)
    try:
        Attribute.query.filter_by(id=Attribute.get('id')).update(attribute)
        return jsonify(Attribute.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@attributes.route('/api/attributes', methods=['DELETE'])
def delete_attributes():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(Attribute).filter(Attribute.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def attributes_validate_required(Attribute):
    errors = []
    for attr in ('name', 'value_list', 'attribute_type', 'attribute_type', 'order'):
        if not Attribute.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'attributes',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True