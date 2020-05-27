
from flask import request, redirect
from flask_restplus import Resource

from ..util.decorator import admin_token_required

from ..util.dto import UserDto
from ..service.user_service import save, get_all, get_one, confirm, remove, validate_payload

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @admin_token_required
    @api.marshal_list_with(_user)
    def get(self):
        """ Список зарегистрированных пользователей """
        return get_all()

    @api.expect(_user)
    @api.response(201, 'Пользователь успешно создан.')
    def post(self):
        """ Регистрация нового пользователя """
        v = validate_payload(self.api.payload, _user)
        if v:
            return v
        else:
            return save(data = request.json)


@api.route('/<public_id>')
@api.response(401, 'Пользователь не найден.')
class User(Resource):
    @api.marshal_with(_user)
    def get(self, public_id):
        """ Получить информацию о пользователе по его идентификатору """
        user = get_one(public_id)
        if not user:
            api.abort(401)
        else:
            return user


    @api.response(401, 'Пользователь не найден.')
    def delete(self, public_id):
        """Удаление пользователя """
        return remove(public_id)



@api.route('/confirmation/<public_id>')
@api.response(401, 'Пользователь не найден.')
class User(Resource):
    def get(self, public_id):
        confirm(public_id)
        
        return redirect('https://medtrading.org/')


