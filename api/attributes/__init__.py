from flask import (Blueprint, jsonify, request)
from models import Attribute, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc
from pypnusershub import routes as fnauth

attributes = Blueprint('attributes', __name__)


@attributes.route('/api/attributes', methods=['GET'])
@fnauth.check_auth(4)
def get_attributes():
    try:
        attributes = Attribute.query.\
            order_by(desc(Attribute.id)). \
            all()
        return jsonify([Attribute.json() for Attribute in attributes])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


@attributes.route('/api/attributes/<int:id>', methods=['GET'])
@fnauth.check_auth(4)
def get_attribute_by_id(id=id):
    try:
        attribute = Attribute.query.get(id)
        if attribute:
            return jsonify(attribute.json())
        else:
            return 'error not found'
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


@attributes.route('/api/attributes', methods=['POST'])
@fnauth.check_auth(4)
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
@fnauth.check_auth(4)
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
        id = int(payload['id'])
        del payload['id']
        db.session.query(Attribute).filter(Attribute.id == id).update(payload)
        db.session.commit()
        return jsonify(attribute.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()


@attributes.route('/api/attributes', methods=['DELETE'])
@fnauth.check_auth(4)
def delete_attributes():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            db.session.query(Attribute).filter(
                Attribute.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def attributes_validate_required(attribute):
    errors = []
    # required fields
    for attr in ('name', 'attribute_type', 'value_list', 'attribute_type', 'order'):
        if not attribute.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'attributes',
                'column': attr
            })
    # name must be unique        
    name = attribute.get('name').lower()
    name = name.strip()
    attribute_exist = Attribute.query.filter(Attribute.name == name).first()
    if (attribute_exist and (attribute_exist.json().get('id') != attribute.get('id'))):
        errors.append({
            'name': 'attribute_already_exists',
            'table': 'attributes',
            'column': 'name'
        })
    # order must be unique 
    order = attribute.get('order')
    order_exist = Attribute.query.filter(Attribute.order == order).first()
    if (order_exist  and (order_exist.json().get('id') != attribute.get('id'))):
        errors.append({
            'name': 'order_already_exists',
            'table': 'attributes',
            'column': 'order'
        })
    if len(errors) >= 0:
        return {'errors': errors}

    return True
