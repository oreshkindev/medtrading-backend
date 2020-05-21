
from .. import db

import datetime


class Callto(db.Model):
    """ Модель заявок """
    __tablename__ = "callto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<User '{}'>".format(self.registered_on)
