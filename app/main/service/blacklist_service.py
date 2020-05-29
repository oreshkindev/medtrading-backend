
from app.main import db

from app.main.model.blacklist import BlacklistToken


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        try:
            db.session.commit()
        except Exception as e:
            session.rollback()
        response_object = {
            'status': 'success',
            'message': 'Успешное завершение сеанса.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200
