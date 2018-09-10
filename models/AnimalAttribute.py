from . import db
from datetime import datetime


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
        return '<Boat %r>' % self.name

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