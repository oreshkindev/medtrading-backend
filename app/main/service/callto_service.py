import uuid
import datetime

from app.main import db, mail
from app.main.model.callto import Callto

from flask_mail import Message

def save_new_callto(data):
    phone = data.get('phone')
    if not phone:
        response_object = {
            'status': 'fail',
            'message': 'Не указан номер телефона',
        }
        return response_object, 409
    new_callto = Callto(
        name=data['name'],
        phone=data['phone'],
        registered_on=datetime.datetime.utcnow()
    )
    save_changes(new_callto)

    msg = Message("Запрос на сайте Medtrading.org",
                sender=('Medtrading Support', current_app.config['MAIL_USERNAME']),
                html = render_template('callto_email.html', name=data['name'], phone=data['phone'], registered_on=new_callto.registered_on),
                recipients=[current_app.config['MAIL_USERNAME']])
    mail.send(msg)

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
