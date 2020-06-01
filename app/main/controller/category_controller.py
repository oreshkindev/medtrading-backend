
from flask import request
from flask_restplus import Resource

from ..util.decorator import admin_token_required
from ..util.dto import CategoryDto
from ..service.category_service import save, get_all, get_one, update, remove, validate_payload

api = CategoryDto.api
_category = CategoryDto.category


@api.route('/')
class CategoryList(Resource):
    @api.marshal_list_with(_category)
    def get(self):
        """ Список зарегистрированных категорий """
        return get_all()

    @admin_token_required
    @api.expect(_category)
    @api.response(201, 'Категория успешно создана.')
    @api.response(401, 'Проверьте введенные данные. Все поля должны быть заполнены.')
    def post(self):
        """ Регистрация новой категории """
        v = validate_payload(self.api.payload, _category)
        if v:
            return v
        else:
            return save(data = request.json)


@api.route('/<public_id>')
@api.response(404, 'Категория не найдена.')
class Category(Resource):
    @api.marshal_with(_category)
    def get(self, public_id):
        """ Получить категорию по ее идентификатору """
        category = get_one(public_id)
        if not category:
            api.abort(404)
        else:
            return category

    @api.response(201, 'Категория успешно обновлена.')
    def put(self, public_id):
        """ Обновление категории """
        v = validate_payload(self.api.payload, _category)
        if v:
            return v
        else:
            return update(public_id, request.json)


    @api.response(201, 'Категория успешно удалена.')
    def delete(self, public_id):
        """ Удаление категории """
        return remove(public_id)



