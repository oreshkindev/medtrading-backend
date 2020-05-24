
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'name': fields.String(description='The user name'),
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'phone': fields.String(description='user phone'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'name': fields.String(required=True, description='The product name'),
        'public_name': fields.String(description='The product name'),
        'description': fields.String(description='The product name'),
        'body': fields.String(description='The body name'),
        'price': fields.String(required=True, description='product price'),
        'quantity': fields.String(required=True, description='product quantity'),
        'batch_id': fields.String(description='product Identifier'),
        'category_id': fields.String(description='product category Identifier'),
        'manufacturer': fields.String(required=True, description='product manufacturer Identifier'),
        'country': fields.String(required=True, description='product country Identifier'),
        'weight': fields.String(required=True, description='product weight Identifier'),
        'minimal_order': fields.String(required=True, description='product minimal order Identifier'),
        'image': fields.String(description='product Identifier'),
    })


class CategoryDto:
    api = Namespace('category', description='category related operations')
    category = api.model('category', {
        'name': fields.String(required=True, description='category name'),
        'public_name': fields.String(description='category Slug'),
        'public_id': fields.String(description='category Identifier'),
        'description': fields.String(description='category description'),
        'image': fields.String(description='product Identifier'),
    })


class CheckoutDto:
    api = Namespace('checkout', description='checkout related operations')
    checkout = api.model('checkout', {
        'name': fields.String(description='checkout Identifier'),
        'email': fields.String(description='checkout Identifier'),
        'positions': fields.String(description='checkout positions'),
        'total': fields.Float(description='checkout total'),
        'status': fields.String(description='checkout status'),
        'batch_id': fields.String(description='checkout batch_id'),
        'description': fields.String(description='checkout description'),
    })


class CalltoDto:
    api = Namespace('callto', description='callto related operations')
    callto = api.model('callto', {
        'name': fields.String(required=True, description='caller username'),
        'phone': fields.String(required=True, description='caller phone'),
    })
