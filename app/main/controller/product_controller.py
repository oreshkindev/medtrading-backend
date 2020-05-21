
from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductDto
from ..service.product_service import save_new_product, get_all_products, get_a_product, remove_a_product

api = ProductDto.api
_product = ProductDto.product


@api.route('/')
class ProductList(Resource):
    @api.doc('list_of_registered_products')
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """ Список зарегистрированных товаров """
        return get_all_products()

    @admin_token_required
    @api.expect(_product, validate=True)
    @api.response(201, 'Товар успешно создан.')
    @api.doc('create a new product')
    def post(self):
        """ Регистрация нового товара """
        data = request.json
        return save_new_product(data=data)


@api.route('/<batch_id>')
@api.param('batch_id', 'Идентификатор товара')
@api.response(404, 'Товар не найден.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, batch_id):
        """ Получить товар по его идентификатору """
        product = get_a_product(batch_id)
        if not product:
            api.abort(404)
        else:
            return product


@api.route('/remove/')
@api.response(404, 'Товар не найден')
class Product(Resource):
    @api.doc('get a product')
    def post(self):
        """ Удаление товара """
        data = request.json
        return remove_a_product(data=data)



