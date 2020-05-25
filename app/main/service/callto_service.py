import uuid, datetime

from app.main import db
from app.main.model.callto import Callto
from app.main.util.email import send_callto_email

def save_new_callto(data):
    phone = data.get('phone')
    if not phone:
        response_object = {
            'status': 'fail',
            'message': 'Не указан номер телефона',
        }
        return response_object, 409
    callto = Callto(
        name=data['name'],
        phone=data['phone'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(callto)

    send_callto_email(callto)

    response_object = {
        'status': 'success',
        'message': 'Заявка успешно добавлена.'
    }
    return response_object, 201


def get_all_calltos():
    return Callto.query.all()


def get_a_callto(phone):
    return Callto.query.filter_by(phone=phone).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
