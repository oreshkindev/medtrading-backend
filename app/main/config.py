
import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

# production path /var/www/medtrading-frontend/dist/img
# development path D:/development/medtrading-frontend/src/assets/images

upload = '/var/www/medtrading-frontend/dist/img'

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'f7b93a0615d24ac1a773b5de5158673c')
    DEBUG = False
    # mail settings
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'info@medtrading.org'
    MAIL_PASSWORD = 'Q12345678q'
    MANAGER_MAIL = 'admin@medtrading.org'

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'medtrading.db')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 30
    SQLALCHEMY_POOL_PRE_PING = True

class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
