from flask import Flask


from App.house_views import house
from App.fuck import fuck
from App.order_views import order
from App.views import user
from utils.functions import init_ext
from utils.settings import templates_dir, static_dir


def create_app(config):
    app = Flask(__name__,
                template_folder=templates_dir,
                static_folder=static_dir)

    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house, url_prefix='/house')
    app.register_blueprint(blueprint=order, url_prefix='/order')
    app.register_blueprint(blueprint=fuck)

    app.config.from_object(config)
    init_ext(app)
    return app
