from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DUPLICATE_KEY_ERROR_REGEX = r'DETAIL:\s+Key \((?P<duplicate_key>.*)\)=\(.*\) already exists.'

db = SQLAlchemy()
migrate = Migrate()
from . import Analysis, Animal, Attribute, AnimalAttribute, AnimalDevice, Device, DeviceType