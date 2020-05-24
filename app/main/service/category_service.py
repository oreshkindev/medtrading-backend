
import os, base64, random

from app.main.model.category import Category
from app.main import db
from app.main.config import upload
from slugify import slugify


def save_category(data):

    category = Category(
        public_id=generate_random_number(4),
        public_name=slugify(data['name']),
        name=data['name'],
        description=data['description'],
        image=slugify(data['name']) + '.png'
    )

    set_image(data['image'], data['name'])

    save_changes(category)

    response_object = {
        'status': 'success',
        'message': 'Категория успешно добавлена.'
    }
    return response_object, 201


def update_category(public_id, data):

    get_category = Category.query.filter_by(public_id=public_id).first()

    # generate data image from base64
    set_image(data['image'], data['name'], oldname=get_category.image)

    category = Category.query.filter_by(public_id=public_id).update(
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
    
def set_image(image, name, oldname=None):
    if image == oldname:
        os.rename(os.path.join(upload + '/category/', oldname),os.path.join(upload + '/category/', slugify(name) + '.png'))

    else:
        if oldname:
            os.remove(os.path.join(upload + '/category/', oldname))
        # generate data image from base64
        base64_message = image[image.index(',') + 1:]
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)

        image_file = open(upload + '/category/' + slugify(name) + '.png', 'wb')
        image_file.write(message_bytes)
        image_file.close()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))


def remove_a_category(public_id):
    category = Category.query.filter_by(public_id=public_id).first()
    if not category:
        response_object = {
            'status': 'fail',
            'message': 'Такой категории нет в системе.',
        }
        return response_object, 409
    else:
        os.remove(os.path.join(upload + '/category/', category.public_name + '.png'))

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