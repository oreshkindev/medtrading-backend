
from flask import request
from flask_restplus import Resource

from ..util.decorator import admin_token_required
from ..util.dto import CallbackDto
from ..service.callback_service import save, get_all, remove, validate_payload

api = CallbackDto.api
_callback = CallbackDto.callback


@api.route('/')
class CallbackList(Resource):
    @admin_token_required
    @api.marshal_list_with(_callback)
    def get(self):
        """ Список зарегистрированных заявок """
        return get_all()

    @api.expect(_callback)
    @api.response(200, 'Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
    @api.response(400, 'Проверьте введенные данные. Все поля должны быть заполнены.')
    def post(self):
        """ Регистрация новой заявки """
        v = validate_payload(self.api.payload, _callback)
        if v:
            return v
        else:
            return save(data = request.json)


@api.route('/<id>')
@api.response(200, 'Заявка успешно удалена.')
@api.response(400, 'Такой заявки нет в системе.')
class Callback(Resource):
    @admin_token_required
    def delete(self, id):
        """ Удаление заявки """
        return remove(id)

