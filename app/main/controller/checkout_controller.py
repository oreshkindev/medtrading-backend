
from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import CheckoutDto
from ..service.checkout_service import save, get_all, get_one, update, remove

api = CheckoutDto.api
_checkout = CheckoutDto.checkout


@api.route('/')
class CheckoutList(Resource):
    @admin_token_required
    @api.marshal_list_with(_checkout)
    def get(self):
        """ Список зарегистрированных заказов """
        return get_all()

    @token_required
    @api.expect(_checkout)
    @api.response(201, 'Заказ успешно создан.')
    def post(self):
        """ Регистрация нового заказа """
        return save(data = request.json)


@api.route('/<batch_id>')
@api.response(404, 'Заказ не найден.')
class Checkout(Resource):
    @token_required
    @api.marshal_with(_checkout)
    def get(self, batch_id):
        """ Получить заказ по его идентификатору """
        checkout = get_one(batch_id)
        if not checkout:
            api.abort(404)
        else:
            return checkout

    @api.response(404, 'Заказ не найден.')
    def put(self, batch_id):
        """ Обновление заказа """
        return update(batch_id, request.json)


    @api.response(404, 'Заказ не найден.')
    def delete(self, batch_id):
        """Удаление заказа """
        return remove(batch_id)
