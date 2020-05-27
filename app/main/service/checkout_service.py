
import datetime, random

from .. import db
from ..model.checkout import Checkout
from ..util.email import send_checkout_email, send_checkout_admin


def save(data):
    this = Checkout (
        batch_id = generate_random_number(6),
        email = data['email'],
        name = data['name'],
        phone = data['phone'],
        positions = str(data['positions']),
        total = data['total'],

        created_on=datetime.datetime.utcnow()
    )

    db.session.add(this)
    db.session.commit()

    send_checkout_email(this, data['positions'])

    send_checkout_admin(this, data['positions'])

    response_object = {
        'status': 'success',
        'message': 'Заказ успешно добавлен.'
    }
    return response_object, 201


def update(batch_id, data):

    Checkout.query.filter_by(batch_id = batch_id).update(
        dict(
            name = data['name'],
            phone = data['phone'],
            status = bool(data['status']),
        )
    )

    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Заказ обновлен.',
    }
    return response_object, 201


def remove(batch_id):
    this = Checkout.query.filter_by(batch_id=batch_id).first()

    if not this:
        response_object = {
            'status': 'fail',
            'message': 'Такого заказа нет в системе.',
        }
        return response_object, 409
    else:
        db.session.delete(this)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Заказ успешно удален.'
        }
        return response_object, 201


def get_all():
    return Checkout.query.all()


def get_one(email):
    return Checkout.query.filter_by(email = email).all()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))