
from .. import db


class Category(db.Model):
    """ Модель категорий """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    public_name = db.Column(db.String(255), unique=True)
    public_id = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String(100))

    def __repr__(self):
        return "<Category '{}'>".format(self.name)
