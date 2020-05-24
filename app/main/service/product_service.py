
import os, datetime, base64, random

from app.main.model.product import Product
from app.main import db
from app.main.config import upload
from slugify import slugify


def save_product(data):

        product = Product(
            name = data['name'],
            public_name = slugify(data['name']),
            description = data['description'],
            body = data['body'],
            price = data['price'],
            quantity = data['quantity'],
            batch_id = generate_random_number(6),
            category_id = data['category_id'],
            manufacturer = data['manufacturer'],
            country = data['country'],
            minimal_order = data['minimal_order'],
            weight = data['weight'],
            image = slugify(data['name']) + '.png',
            created_on = datetime.datetime.utcnow()
        )

        set_image(data['image'], data['name'])

        save_changes(product)

        response_object = {
            'status': 'success',
            'message': 'Товар успешно добавлен.'
        }
        return response_object, 201


def update_product(batch_id, data):

            get_product = Product.query.filter_by(batch_id=batch_id).first()

            # generate data image from base64
            set_image(data['image'], data['name'], oldname=get_product.image)

            product = Product.query.filter_by(batch_id=batch_id).update(
                dict(
                    name=data['name'],
                    public_name=slugify(data['name']),
                    description=data['description'],
                    body=data['body'],
                    price=data['price'],
                    quantity=data['quantity'],
                    batch_id=data['batch_id'],
                    category_id=data['category_id'],
                    manufacturer=data['manufacturer'],
                    country=data['country'],
                    minimal_order=data['minimal_order'],
                    weight=data['weight'],
                    image=slugify(data['name']) + '.png'
                )
            )

            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Товар обновлен.',
            }
            return response_object, 201

def get_all_products():
    return Product.query.all()


def get_a_product(batch_id):
    return Product.query.filter_by(batch_id=batch_id).first()
    
def set_image(image, name, oldname=None):
    if image == oldname:
        os.rename(os.path.join(upload + '/product/', oldname),os.path.join(upload + '/product/', slugify(name) + '.png'))

    else:
        if oldname:
            os.remove(os.path.join(upload + '/product/', oldname))
        # generate data image from base64
        base64_message = image[image.index(',') + 1:]
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)

        image_file = open(upload + '/product/' + slugify(name) + '.png', 'wb')
        image_file.write(message_bytes)
        image_file.close()


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))


def remove_a_product(batch_id):
    product = Product.query.filter_by(batch_id=batch_id).first()
    if not product:
        response_object = {
            'status': 'fail',
            'message': 'Такого товара нет в системе.',
        }
        return response_object, 409
    else:
        os.remove(os.path.join(upload + '/product/', product.public_name + '.png'))

        remove_changes(product)

        response_object = {
            'status': 'success',
            'message': 'Товар успешно удален.'
        }
        return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def remove_changes(data):
    db.session.delete(data)
    db.session.commit()
