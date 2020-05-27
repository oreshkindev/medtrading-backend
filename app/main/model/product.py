
from .. import db

import datetime


class Product(db.Model):
    """ Модель товаров """
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    public_name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    body = db.Column(db.Text)
    price = db.Column(db.Float)
    quantity = db.Column(db.String(100))
    batch_id = db.Column(db.String(100), unique=True)
    category_id = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    country = db.Column(db.String(100))
    minimal_order = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    image = db.Column(db.String(100))
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
