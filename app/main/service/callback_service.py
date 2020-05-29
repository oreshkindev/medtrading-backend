import uuid, datetime

from .. import db
from ..model.callback import Callback
from ..util.email import send_callback_email

def save(data):

    this = Callback (
        name = data['name'],
        phone = data['phone'],

        registered_on = datetime.datetime.utcnow()
    )

    db.session.add(this)
    try:
        db.session.commit()
    except Exception as e:
        session.rollback()

    send_callback_email(this)

    response_object = {
        'status': 'success',
        'message': 'Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.'
    }
    return response_object, 200


def get_all():
    return Callback.query.all()


def get_one(phone):
    return Callback.query.filter_by(phone = phone).first()


def remove(id):
    this = Callback.query.filter_by(id = id).first()

    if not this:
        response_object = {
            'status': 'fail',
            'message': 'Такой заявки нет в системе.',
        }
        return response_object, 400
    else:
        db.session.delete(this)
        try:
            db.session.commit()
        except Exception as e:
            session.rollback()

        response_object = {
            'status': 'success',
            'message': 'Заявка успешно удалена.'
        }
        return response_object, 200


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
