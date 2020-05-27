from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from app.main import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, body):
    app = current_app._get_current_object()

    msg = Message(subject, sender = sender, recipients = recipients)
    msg.html = body
    Thread(target = send_async_email, args = (app, msg)).start()


def send_checkout_email(user, data):
    send_email('Статус заказа на сайте Medtrading.org',
               sender = ('Medtrading Support', current_app.config['MAIL_USERNAME']),
               recipients = [user.email],
               body = render_template('checkout_email.html', name = user.name, batch_id = user.batch_id, positions = data, total = user.total, created_on = user.created_on))


def send_checkout_admin(user, data):
    send_email('Новый заказ на сайте Medtrading.org',
               sender = ('Medtrading Support', current_app.config['MAIL_USERNAME']),
               recipients = [current_app.config['MANAGER_MAIL']],
               body = render_template('checkout_admin_email.html', name = user.name, phone = user.phone, batch_id = user.batch_id, positions = data, total = user.total, created_on = user.created_on))


def send_callback_email(user):
    send_email('Запрос на сайте Medtrading.org',
               sender = ('Medtrading Support', current_app.config['MAIL_USERNAME']),
               recipients = [current_app.config['MANAGER_MAIL']],
               body = render_template('callto_email.html', name=user.name, phone=user.phone, registered_on=user.registered_on))


def send_register_email(user):
    send_email('Подтверждение аккаунта на сайте Medtrading.org',
               sender = ('Medtrading Support', current_app.config['MAIL_USERNAME']),
               recipients = [user.email],
               body = render_template('follower_email.html', confirm_url=user.public_id))
