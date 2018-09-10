from . import db
from datetime import datetime


class DeviceType(db.Model):

    __tablename__ = 'device_types'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Boat %r>' % self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }