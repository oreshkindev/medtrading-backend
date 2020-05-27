
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user')
    user = api.model('user', {
        'email': fields.String(required=True),
        'name': fields.String(required=True),
        'password': fields.String(required=True),
        'phone': fields.String(),
        'public_id': fields.String()
    })


class AuthDto:
    api = Namespace('auth')
    user_auth = api.model('user_auth', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
    })


class ProductDto:
    api = Namespace('product')
    product = api.model('product', {
        'batch_id': fields.String(),
        'body': fields.String(required=True),
        'category_id': fields.String(required=True),
        'country': fields.String(required=True),
        'description': fields.String(required=True),
        'image': fields.String(required=True),
        'name': fields.String(required=True),
        'manufacturer': fields.String(required=True,),
        'minimal_order': fields.String(required=True,),
        'price': fields.String(required=True),
        'public_name': fields.String(),
        'quantity': fields.String(required=True),
        'weight': fields.String(required=True),
    })


class CategoryDto:
    api = Namespace('category')
    category = api.model('category', {
        'description': fields.String(required=True),
        'image': fields.String(required=True),
        'name': fields.String(required=True),
        'public_name': fields.String(),
        'public_id': fields.String(),
    })


class CheckoutDto:
    api = Namespace('checkout')
    checkout = api.model('checkout', {
        'batch_id': fields.String(),
        'email': fields.String(),
        'name': fields.String(),
        'phone': fields.String(),
        'positions': fields.String(),
        'status': fields.Boolean(),
        'total': fields.Float(),
    })


class CallbackDto:
    api = Namespace('callback')
    callback = api.model('callback', {
        'id': fields.Integer(),
        'name': fields.String(required=True),
        'phone': fields.String(required=True),
    })
