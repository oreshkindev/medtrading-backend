
from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import CheckoutDto
from ..service.checkout_service import save_new_checkout, get_all_checkouts, get_a_checkout

api = CheckoutDto.api
_checkout = CheckoutDto.checkout


@api.route('/')
class CheckoutList(Resource):
    @api.doc('list_of_registered_checkouts')
    @admin_token_required
    @api.marshal_list_with(_checkout, envelope='data')
    def get(self):
        """ Список зарегистрированных заказов """
        return get_all_checkouts()

    @token_required
    @api.expect(_checkout, validate=False)
    @api.response(201, 'Заказ успешно создан.')
    @api.doc('create a new checkout')
    def post(self):
        """ Регистрация нового заказа """
        data = request.json
        return save_new_checkout(data=data)


@api.route('/<batch_id>')
@api.param('batch_id', 'Идентификатор заказа')
@api.response(404, 'Заказ не найден.')
class Checkout(Resource):
    @api.doc('get a checkout')
    @token_required
    @api.marshal_with(_checkout)
    def get(self, batch_id):
        """ Получить заказ по его идентификатору """
        checkout = get_a_checkout(batch_id)
        if not checkout:
            api.abort(404)
        else:
            return checkout
