
import os, datetime, base64, random

from ..model.product import Product
from .. import db
from ..config import upload
from slugify import slugify

def save(data):

    this = Product (
        batch_id = generate_random_number(6),
        body = data['body'],
        category_id = data['category_id'],
        country = data['country'],
        created_on = datetime.datetime.utcnow(),
        description = data['description'],
        image = slugify(data['name']) + '.png',
        manufacturer = data['manufacturer'],
        minimal_order = data['minimal_order'],
        name = data['name'],
        public_name = slugify(data['name']),
        price = data['price'],
        quantity = data['quantity'],
        weight = data['weight']
    )

    find = Product.query.filter_by(public_name = this.public_name).first()
    if find:
        response_object = {
            'status': 'fail',
            'message': 'Такой товар уже есть в системе.'
        }
        return response_object, 401
    else:
        set_image(data['image'], data['name'])

        db.session.add(this)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Товар успешно добавлен.'
        }
        return response_object, 201


def update(batch_id, data):

    this = Product.query.filter_by(batch_id = batch_id).first()

    # generate data image from base64
    set_image(data['image'], data['name'], oldname = this.image)

    Product.query.filter_by(batch_id = batch_id).update(
        dict(
            batch_id = data['batch_id'],
            body = data['body'],
            category_id = data['category_id'],
            country = data['country'],
            description = data['description'],
            image = slugify(data['name']) + '.png',
            manufacturer = data['manufacturer'],
            minimal_order = data['minimal_order'],
            name = data['name'],
            public_name = slugify(data['name']),
            price = data['price'],
            quantity = data['quantity'],
            weight = data['weight']
        )
    )

    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Товар обновлен.',
    }
    return response_object, 201

def get_all():
    db.session.close()
    return Product.query.all()


def get_one(batch_id):
    return Product.query.filter_by(batch_id = batch_id).first()
    
def set_image(image, name, oldname = None):
    if image == oldname:
        os.rename(os.path.join(upload + '/product/', oldname),os.path.join(upload + '/product/', slugify(name) + '.png'))

    else:
        # if oldname:
        #     os.remove(os.path.join(upload + '/product/', oldname))

        base64_message = image[image.index(',') + 1:]
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)

        image_file = open(upload + '/product/' + slugify(name) + '.png', 'wb')
        image_file.write(message_bytes)
        image_file.close()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))


def remove(batch_id):
    this = Product.query.filter_by(batch_id = batch_id).first()

    if not this:
        response_object = {
            'status': 'fail',
            'message': 'Такого товара нет в системе.',
        }
        return response_object, 409
    else:
        os.remove(os.path.join(upload + '/product/', this.public_name + '.png'))

        db.session.delete(this)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Товар успешно удален.'
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