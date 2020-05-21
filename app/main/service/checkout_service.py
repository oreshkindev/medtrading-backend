import uuid
import datetime

from app.main import db
from app.main.model.checkout import Checkout

from flask_mail import Message
from app.main import mail
from flask import render_template
from flask import current_app


def save_new_checkout(data):
    new_checkout = Checkout(
        batch_id=str(uuid.uuid1()),
        email=data['email'],
        name=data['name'],
        description=data['description'],
        positions=str(data['positions']),
        total=data['total'],
        created_on=datetime.datetime.utcnow()
    )
    save_changes(new_checkout)


    msg = Message("Статус заказа на сайте Medtrading.org",
                sender=('Medtrading Support', current_app.config['MAIL_USERNAME']),
                html = render_template('checkout_email.html', name=data['name'], batch_id=new_checkout.batch_id, positions=data['positions'], total=data['total'], created_on=new_checkout.created_on),
                recipients=["oreshkin.dev@outlook.com"])
    mail.send(msg)

    response_object = {
        'status': 'success',
        'message': 'Заказ успешно добавлен.'
    }
    return response_object, 201


def get_all_checkouts():
    return Checkout.query.all()


def get_a_checkout(email):
    return Checkout.query.filter_by(email=email).all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
