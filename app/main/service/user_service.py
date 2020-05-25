import uuid, datetime

from flask import render_template, current_app
from app.main import db
from app.main.model.user import User
from app.main.util.email import send_register_email

def save_new_user(data):
    user = User.query.filter_by(email = data['email']).first()
    if not user:
        new_user = User(
            public_id = str(User.encode_auth_token(data['email'])),
            email = data['email'],
            name = data['name'],
            password = data['password'],
            confirmed = False,
            registered_on = datetime.datetime.utcnow()
        )
        save_changes(new_user)

        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Такой пользователь уже есть в системе. Пожалуйста авторизуйтесь.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Пользователь успешно зарегистрирован.',
            'Authorization': auth_token.decode()
        }

        send_register_email(user)

        return response_object, 201

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Произошла какая-то ошибка. Пожалуйста, попробуйте еще раз.'
        }
        return response_object, 401


def user_confirmation(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    update = User.query.filter_by(public_id=public_id).update(
        dict(
            confirmed=True
        )
    )

    db.session.commit()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

