from . import db
from datetime import datetime
from geoalchemy2 import Geometry


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