from . import db
from datetime import datetime


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
            'id': self.id
        }