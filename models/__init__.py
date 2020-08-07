from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from geoalchemy2 import Geometry

DUPLICATE_KEY_ERROR_REGEX = r'DETAIL:\s+Key \((?P<duplicate_key>.*)\)=\(.*\) already exists.'

db = SQLAlchemy()


class Animal(db.Model):

    __tablename__ = 't_animals'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_animal = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer())
    capture_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime,  nullable=True)
    comment = db.Column(db.Text())
    animal_devices = db.relationship('AnimalDevice', backref='animals',
                                     cascade="save-update, delete", lazy='dynamic', foreign_keys='AnimalDevice.id_animal')
    animal_attributes = db.relationship('AnimalAttribute', backref='animals',
                                        cascade="save-update, delete",  lazy='dynamic', foreign_keys='AnimalAttribute.id_animal')

    def json(self):
        return {
            'id_animal': self.id_animal,
            'name': self.name,
            'birth_year': self.birth_year,
            'capture_date': self.capture_date.strftime('%d/%m/%Y'),
            'death_date': self.death_date.strftime('%d/%m/%Y') if self.death_date else None ,
            'comment': self.comment,
            'animal_devices': [animal_device.json() for animal_device in self.animal_devices],
            'animal_attributes': [animal_attribute.json() for animal_attribute in self.animal_attributes],
        }


class Attribute(db.Model):

    __tablename__ = 'lib_attributes'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_attribute = db.Column(db.Integer(), primary_key=True)
    attribute = db.Column(db.String(50))
    value_list = db.Column(db.Text())
    attribute_type = db.Column(db.Text())
    order = db.Column(db.Integer())

    def json(self):
        return {
            'id_attribute': self.id_attribute,
            'attribute': self.attribute,
            'value_list': self.value_list,
            'attribute_type': self.attribute_type,
            'order': self.order
        }


class DeviceType(db.Model):

    __tablename__ = 'lib_device_type'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_device_type = db.Column(db.Integer(), primary_key=True)
    device_type = db.Column(db.String(50), nullable=False)

    def json(self):
        return {
            'id_device_type': self.id_device_type,
            'device_type': self.device_type
        }


class Device(db.Model):

    __tablename__ = 't_devices'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_device = db.Column(db.Integer(), primary_key=True)
    ref_device = db.Column(db.String(50), nullable=False)
    id_device_type = db.Column(db.Integer(), db.ForeignKey(
        'followdem.lib_device_type.id_device_type'), nullable=True)
    comment = db.Column(db.Text())
    device_type = db.relationship('DeviceType')

    def json(self):
        return {
            'id_device': self.id_device,
            'ref_device': self.ref_device,
            'comment': self.comment,
            'device_type': self.device_type.json(),
        }


class AnimalDevice(db.Model):

    __tablename__ = 'cor_animal_devices'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_cor_ad = db.Column(db.Integer(), primary_key=True)
    id_animal = db.Column(db.Integer(), db.ForeignKey(
        'followdem.t_animals.id_animal', ondelete='CASCADE'), nullable=True)
    id_device = db.Column(db.Integer(), db.ForeignKey(
        'followdem.t_devices.id_device'), nullable=True)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    comment = db.Column(db.Text())

    device = db.relationship('Device')

    def json(self):
        return {
            'id_cor_ad': self.id_cor_ad,
            'date_start': self.date_start.strftime('%d/%m/%Y'),
            'date_end': self.date_end.strftime('%d/%m/%Y') if self.date_end else None,
            'comment': self.comment,
            'device': self.device.json()
        }


class AnimalAttribute(db.Model):

    __tablename__ = 'cor_animal_attributes'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_cor_an_att = db.Column(db.Integer(), primary_key=True)
    id_animal = db.Column(db.Integer(), db.ForeignKey(
        'followdem.t_animals.id_animal', ondelete='CASCADE'), nullable=True)
    id_attribute = db.Column(db.Integer(), db.ForeignKey(
        'followdem.lib_attributes.id_attribute'), nullable=True)
    value = db.Column(db.Text())

    attribute = db.relationship('Attribute')

    def json(self):
        return {
            'id_cor_an_att': self.id_cor_an_att,
            'value': self.value,
            'attribute': self.attribute.json()
        }


class Gps_data(db.Model):

    __tablename__ = 't_gps_data'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_gps_data = db.Column(db.Integer(), primary_key=True)
    id_device = db.Column(db.Integer(), db.ForeignKey(
        'followdem.t_devices.id_device'), nullable=True)
    gps_date = db.Column(db.DateTime)
    ttf = db.Column(db.Integer())
    temperature = db.Column(db.Integer())
    sat_number = db.Column(db.Integer())
    hadop = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    altitude = db.Column(db.Integer())
    dimension = db.Column(db.String(50))
    accurate = db.Column(db.Boolean())

    def json(self):
        return {
            'id_gps_data': self.id_gps_data
        }


class Logs(db.Model):

    __tablename__ = 't_logs'
    __table_args__ = {'extend_existing': True, u'schema': 'followdem'}

    id_log = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    log = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def json(self):
        return {
            'id_log': self.id_log,
            'date': self.date,
            'log': self.log
        }
