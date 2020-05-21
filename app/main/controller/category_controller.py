
from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CategoryDto
from ..service.category_service import save_new_category, get_all_categorys, get_a_category, remove_a_category

api = CategoryDto.api
_category = CategoryDto.category


@api.route('/')
class CategoryList(Resource):
    @api.doc('list_of_registered_categorys')
    @api.marshal_list_with(_category, envelope='data')
    def get(self):
        """ Список зарегистрированных категорий """
        return get_all_categorys()

    @admin_token_required
    @api.expect(_category, validate=True)
    @api.response(201, 'Категория успешно создана.')
    @api.doc('create a new category')
    def post(self):
        """ Регистрация новой категории """
        data = request.json
        return save_new_category(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'Идентификатор категории')
@api.response(404, 'Категория не найдена.')
class Category(Resource):
    @api.doc('get a category')
    @api.marshal_with(_category, mask=False)
    def get(self, public_id):
        """ Получить категорию по ее идентификатору """
        category = get_a_category(public_id)
        if not category:
            api.abort(404)
        else:
            return category


@api.route('/remove/')
@api.response(404, 'Category not found.')
class Category(Resource):
    @api.doc('get a category')
    def post(self):
        """Remove a new category """
        data = request.json
        return remove_a_category(data=data)
