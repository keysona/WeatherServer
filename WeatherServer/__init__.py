import yaml
from flask import Flask
from flask_mongoengine import MongoEngine


def create_app(setting_path=None):
    app = Flask(__name__, static_folder='./static')
    if setting_path is None:
        import os
        setting_path = os.path.join(os.path.dirname(__file__), 'setting.yaml')
    with open(setting_path) as f:
        setting = yaml.safe_load(f.read())
        app.config.update(setting['config'])
    return app


def register_blueprints(app):
    from .api import api
    from .weather import weather
    app.register_blueprint(api)
    app.register_blueprint(weather)


def register_filters(app):
    from .filters import get_image_name, format_time,\
                         get_aqi_type, get_aqi_tips
    app.jinja_env.filters['get_image_name'] = get_image_name
    app.jinja_env.filters['format_time'] = format_time
    app.jinja_env.filters['get_aqi_type'] = get_aqi_type
    app.jinja_env.filters['get_aqi_tips'] = get_aqi_tips


def register_admin(app):
    from .admin import create_admin, init_login
    admin = create_admin(name='weather', template_mode='bootstrap3')
    admin.init_app(app)
    init_login(app)


app = create_app()
db = MongoEngine(app)

# register
register_blueprints(app)
register_filters(app)
register_admin(app)

if __name__ == '__main__':
    app.run()
