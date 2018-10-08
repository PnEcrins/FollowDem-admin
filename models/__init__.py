from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from geoalchemy2 import Geometry

DUPLICATE_KEY_ERROR_REGEX = r'DETAIL:\s+Key \((?P<duplicate_key>.*)\)=\(.*\) already exists.'

db = SQLAlchemy()
migrate = Migrate()

class Animal(db.Model):

    __tablename__ = 'animals'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.DateTime)
    capture_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Animal %r>' % self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'capture_date': self.capture_date,
            'death_date': self.death_date,
            'comment': self.comment
        }

class Attribute(db.Model):

    __tablename__ = 'Attributes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    value_list = db.Column(db.Text())
    attribute_type = db.Column(db.Text())
    order = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Attribute %r>' % self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'value_list': self.value_list,
            'attribute_type': self.attribute_type,
            'order': self.order
        }

class DeviceType(db.Model):

    __tablename__ = 'device_types'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<DeviceType %r>' % self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Device(db.Model):

    __tablename__ = 'devices'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    reference = db.Column(db.String(50), nullable=False)
    device_type_id = db.Column(db.Integer())
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Device %r>' % self.reference

    def json(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'comment': self.comment
        }

class AnimalDevice(db.Model):

    __tablename__ = 'animal_devices'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    animal_id = db.Column(db.Integer())
    device_id = db.Column(db.Integer())
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<AnimalDevice %r>' % self.id

    def json(self):
        return {
            'id': self.id,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'comment': self.comment
        }

class AnimalAttribute(db.Model):

    __tablename__ = 'animal_attributes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    animal_id = db.Column(db.Integer())
    attribute_id = db.Column(db.Integer())
    value = db.Column(db.Text())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<AnimalAttribute %r>' % self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'capture_date': self.capture_date,
            'death_date': self.death_date,
            'comment': self.comment,
            'status': self.status
        }

class Analysis(db.Model):

    __tablename__ = 'analyses'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    device_id = db.Column(db.Integer())
    gps_date = db.Column(db.DateTime)
    ttf = db.Column(db.Integer())
    x = db.Column(db.Float())
    y = db.Column(db.Float())
    temperature = db.Column(db.Integer())
    sat_number = db.Column(db.Integer())
    hadop = db.Column(db.Float())
    altitude = db.Column(db.Integer())
    geom_mp = db.Column(Geometry('POINT'))
    accurate = db.Column(db.Boolean())
    animale_device_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Analysis %r>' % self.id

    def json(self):
        return {
            'id': self.id
        }