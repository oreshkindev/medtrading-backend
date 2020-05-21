
from .. import db


class Category(db.Model):
    """ Модель категорий """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    public_name = db.Column(db.String(255), unique=True, nullable=False)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(100))

    def __repr__(self):
        return "<Category '{}'>".format(self.name)
