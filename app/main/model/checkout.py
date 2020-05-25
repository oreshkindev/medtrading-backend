
from .. import db

import datetime


class Checkout(db.Model):
    """ Модель заказов """
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    positions = db.Column(db.String(255))
    total = db.Column(db.Float)
    status = db.Column(db.Boolean, nullable=False, default=False)
    batch_id = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Checkout '{}'>".format(self.batch_id)
