import redis

from utils.settings import SQLALCHEMY_DATABASE_URI


class Config():
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='47.106.145.176', port=6379, password='xl123456yu')
    SESSION_KEY_PREFIX = 'key:'
