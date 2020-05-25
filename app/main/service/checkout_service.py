import uuid, datetime, random

from app.main import db
from app.main.model.checkout import Checkout
from app.main.util.email import send_checkout_email, send_checkout_admin

from flask import render_template

def save_new_checkout(data):
    checkout = Checkout(
        batch_id=generate_random_number(6),
        email=data['email'],
        name=data['name'],
        phone=data['phone'],
        positions=str(data['positions']),
        total=data['total'],
        created_on=datetime.datetime.utcnow()
    )
    save_changes(checkout)

    send_checkout_email(checkout, data['positions'])

    send_checkout_admin(checkout, data['positions'])

    response_object = {
        'status': 'success',
        'message': 'Заказ успешно добавлен.'
    }
    return response_object, 201


def get_all_checkouts():
    return Checkout.query.all()


def get_a_checkout(email):
    return Checkout.query.filter_by(email=email).all()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))


def save_changes(data):
    db.session.add(data)
    db.session.commit()