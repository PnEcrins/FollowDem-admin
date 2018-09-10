from . import db
from datetime import datetime

class Device(db.Model):

    __tablename__ = 'devices'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    reference = db.Column(db.String(50), nullable=False)
    device_type_id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Device %r>' % self.reference

    def json(self):
        return {
            'id': self.id,
            'reference': self.reference
        }