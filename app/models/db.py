from flask_sqlalchemy import SQLAlchemy
from ..helpers import get_datetime

db = SQLAlchemy()

class Base:
    __abstract__ = True
    id = db.Column(db.Integer(), primary_key=True)
    created_date = db.Column(db.DateTime(), default=get_datetime)
