import os

from utils.functions import get_database_uri

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(Base_DIR, 'templates')
static_dir = os.path.join(Base_DIR, 'static')

DATABASE = {
    'db': 'mysql',
    'driver': 'pymysql',
    'user': 'root',
    'host': '47.106.145.176',
    'port': '3306',
    'password': 'xl123456',
    'name': 'house'
}

SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)
UPLOAD_DIR = os.path.join(os.path.join(Base_DIR, 'static'), 'upload')
