import os
import uuid
import datetime
import base64

from app.main import db
from app.main.model.category import Category
from slugify import slugify


def save_new_category(data):
    category = Category.query.filter_by(public_id=data['public_id']).first()
    if not category:
        # generate data image from base64
        set_image(data['image'], data['name'])

        new_category = Category(
            public_id=data['public_id'],
            public_name=slugify(data['name']),
            name=data['name'],
            description=data['description'],
            image=slugify(data['name']) + '.png'
        )

        save_changes(new_category)

        response_object = {
            'status': 'success',
            'message': 'Категория успешно добавлена.'
        }
        return response_object, 201
    else:
        os.remove(os.path.join('D:/development/medtrading-frontend/src/assets/images/category/', category.public_name + '.png'))

        # generate data image from base64
        set_image(data['image'], data['name'])

        update = Category.query.filter_by(public_id=data['public_id']).update(
            dict(
                public_id=data['public_id'],
                public_name=slugify(data['name']),
                name=data['name'],
                description=data['description'],
                image=slugify(data['name']) + '.png'
            )
        )

        db.session.commit()
     
        response_object = {
            'status': 'success',
            'message': 'Категория обновлена.',
        }
        return response_object, 201


def get_all_categorys():
    return Category.query.all()


def get_a_category(public_id):
    return Category.query.filter_by(public_id=public_id).first()
    
def set_image(image, name):
    # generate data image from base64
    base64_message = image[image.index(',') + 1:]
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)

    image_file = open('D:/development/medtrading-frontend/src/assets/images/category/' + slugify(name) + '.png', 'wb')
    image_file.write(message_bytes)
    image_file.close()


def remove_a_category(data):
    category = Category.query.filter_by(public_id=data['public_id']).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'Такой категории нет в системе.',
        }
        return response_object, 409
    else:
        os.remove(os.path.join('D:/development/medtrading-frontend/src/assets/images/category/', category.public_name + '.png'))

        remove_changes(category)

        response_object = {
            'status': 'success',
            'message': 'Категория успешно удалена.'
        }
        return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def remove_changes(data):
    db.session.delete(data)
    db.session.commit()