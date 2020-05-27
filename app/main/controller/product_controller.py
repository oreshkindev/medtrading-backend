
from flask import request
from flask_restplus import Resource

from ..util.decorator import admin_token_required
from ..util.dto import ProductDto
from ..service.product_service import save, get_all, get_one, update, remove, validate_payload

api = ProductDto.api
_product = ProductDto.product


@api.route('/')
class ProductList(Resource):
    @api.marshal_list_with(_product)
    def get(self):
        """ Список зарегистрированных товаров """
        return get_all()

    @admin_token_required
    @api.expect(_product)
    @api.response(201, 'Товар успешно создан.')
    @api.response(401, 'Проверьте введенные данные. Все поля должны быть заполнены.')
    def post(self):
        """ Регистрация нового товара """
        v = validate_payload(self.api.payload, _product)
        if v:
            return v
        else:
            return save(data = request.json)


@api.route('/<batch_id>')
@api.response(404, 'Товар не найден.')
class Product(Resource):
    @api.marshal_with(_product)
    def get(self, batch_id):
        """ Получить товар по его идентификатору """
        product = get_one(batch_id)
        if not product:
            api.abort(404)
        else:
            return product

    @api.response(201, 'Товар успешно обновлен')
    def put(self, batch_id):
        """ Обновление товара """
        return update(batch_id, request.json)


    @api.response(201, 'Товар успешно удален')
    def delete(self, batch_id):
        """ Удаление товара """
        return remove(batch_id)



