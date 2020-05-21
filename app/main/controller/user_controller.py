from flask import request
from flask_restplus import Resource
from flask import redirect
from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, user_confirmation

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """ Список зарегистрированных пользователей """
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'Пользователь успешно создан.')
    @api.doc('create a new user')
    def post(self):
        """ Регистрация нового пользователя """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'Идентификатор пользователя')
@api.response(404, 'Пользователь не найден.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """ Получить информацию о пользователе по его идентификатору """
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/confirmation/<public_id>')
@api.response(404, 'Пользователь не найден.')
class User(Resource):
    @api.doc('confirm user')
    def get(self, public_id):
        user_confirmation(public_id)
        
        return redirect('https://medtrading.org/')


