
import uuid, datetime

from .. import db
from ..model.user import User
from ..util.email import send_register_email

def save(data):

    find = User.query.filter_by(email = data['email']).first()

    if not find:
        this = User (
            email = data['email'],
            name = data['name'],
            password = data['password'],
            public_id = str(User.encode_auth_token(data['email'])),
            registered_on = datetime.datetime.utcnow()
        )

        db.session.add(this)
        try:
            db.session.commit()
        except Exception as e:
            session.rollback()

        return generate_token(this)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Проверьте введенные данные. Возможно такой пользователь уже есть в системе. Пожалуйста авторизуйтесь.',
        }
        return response_object, 401


def get_all():
    return User.query.all()


def get_one(public_id):
    return User.query.filter_by(public_id = public_id).first()


def generate_token(this):
    try:
        auth_token = User.encode_auth_token(this.id)

        response_object = {
            'status': 'success',
            'message': 'Регистрация прошла успешно. Мы отправили вам письмо с инструкциями по активации вашего аккаунта.',
            'Authorization': auth_token.decode()
        }

        send_register_email(this)

        return response_object, 201

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Произошла какая-то ошибка. Пожалуйста, попробуйте еще раз.'
        }
        return response_object, 401


def confirm(public_id):
    User.query.filter_by(public_id = public_id).update(
        dict(
            confirmed = True
        )
    )

    try:
        db.session.commit()
    except Exception as e:
        session.rollback()


def remove(public_id):
    this = User.query.filter_by(public_id = public_id).first()

    if this.admin == True:
        response_object = {
            'status': 'fail',
            'message': 'Отказано в доступе.',
        }
        return response_object, 401
    else:
        db.session.delete(this)
        try:
            db.session.commit()
        except Exception as e:
            session.rollback()

        response_object = {
            'status': 'success',
            'message': 'Пользователь успешно удален.'
        }
        return response_object, 201


def validate_payload(payload, api_model):
    """
    Validate payload against an api_model. Aborts in case of failure
    - This function is for custom fields as they can't be validated by
      flask restplus automatically.
    - This is to be called at the start of a post or put method
    """
    # check if any reqd fields are missing in payload
    for key in api_model:
        if api_model[key].required and key not in payload:

            response_object = {
                'status': 'fail',
                'message': 'Проверьте введенные данные. Все поля должны быть заполнены.'
            }
            return response_object, 401

    for key in payload:
        if len(payload[key]) == 0:

            response_object = {
                'status': 'fail',
                'message': 'Проверьте введенные данные. Все поля должны быть заполнены.'
            }
            return response_object, 401

