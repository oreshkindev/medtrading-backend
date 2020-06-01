
import os, base64, random

from ..model.category import Category
from .. import db
from ..config import upload
from slugify import slugify

def save(data):

    this = Category (
        description = data['description'],
        image = slugify(data['name']) + '.png',
        name = data['name'],
        public_id = generate_random_number(4),
        public_name = slugify(data['name'])
    )

    find = Category.query.filter_by(public_name = this.public_name).first()
    if find:
        response_object = {
            'status': 'fail',
            'message': 'Такая категория уже есть в системе.'
        }
        return response_object, 401
    else:
        set_image(data['image'], data['name'])

        db.session.add(this)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Категория успешно добавлена.'
        }
        return response_object, 201


def update(public_id, data):

    this = Category.query.filter_by(public_id = public_id).first()

    # generate data image from base64
    set_image(data['image'], data['name'], oldname = this.image)

    Category.query.filter_by(public_id = public_id).update(
        dict(
            description = data['description'],
            image = slugify(data['name']) + '.png',
            name = data['name'],
            public_id = data['public_id'],
            public_name = slugify(data['name'])
        )
    )

    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Категория обновлена.',
    }
    return response_object, 201

def get_all():
    # db.session.close()
    return Category.query.all()


def get_one(public_id):
    return Category.query.filter_by(public_id = public_id).first()
    
def set_image(image, name, oldname = None):
    if image == oldname:
        os.rename(os.path.join(upload + '/category/', oldname),os.path.join(upload + '/category/', slugify(name) + '.png'))

    else:
        # if oldname:
        #     os.remove(os.path.join(upload + '/category/', oldname))

        base64_message = image[image.index(',') + 1:]
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)

        image_file = open(upload + '/category/' + slugify(name) + '.png', 'wb')
        image_file.write(message_bytes)
        image_file.close()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))


def remove(public_id):
    this = Category.query.filter_by(public_id = public_id).first()

    if not this:
        response_object = {
            'status': 'fail',
            'message': 'Такой категории нет в системе.',
        }
        return response_object, 409
    else:
        os.remove(os.path.join(upload + '/category/', this.public_name + '.png'))

        db.session.delete(this)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Категория успешно удалена.'
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