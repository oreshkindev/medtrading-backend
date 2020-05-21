
from .. import db

import datetime


class Product(db.Model):
    """ Модель товаров """
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    public_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    body = db.Column(db.String(255))
    price = db.Column(db.Float(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    batch_id = db.Column(db.String(100), unique=True, nullable=False)
    category_id = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    minimal_order = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
