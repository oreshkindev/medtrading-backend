from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CalltoDto
from ..service.callto_service import save_new_callto, get_all_calltos

api = CalltoDto.api
_callto = CalltoDto.callto


@api.route('/')
class CalltoList(Resource):
    @api.doc('list_of_registered_calltos')
    @admin_token_required
    @api.marshal_list_with(_callto, envelope='data')
    def get(self):
        """ Список зарегистрированных заявок """
        return get_all_calltos()

    @api.expect(_callto, validate=True)
    @api.response(201, 'Заявка успешно создана.')
    @api.doc('create a new callto')
    def post(self):
        """ Регистрация новой заявки """
        data = request.json
        return save_new_callto(data=data)

