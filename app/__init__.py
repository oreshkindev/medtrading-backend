from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.product_controller import api as product_ns
from .main.controller.category_controller import api as category_ns
from .main.controller.checkout_controller import api as checkout_ns
from .main.controller.callto_controller import api as callto_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
          title='MEDTRADING.ORG API',
          version='1.0',
          description='Документация для работы с условными API запросами на сервере'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(product_ns, path='/product')
api.add_namespace(category_ns, path='/category')
api.add_namespace(checkout_ns, path='/checkout')
api.add_namespace(callto_ns, path='/callto')