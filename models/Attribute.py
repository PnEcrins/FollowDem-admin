from . import db
from datetime import datetime

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
            'name': self.name
        }