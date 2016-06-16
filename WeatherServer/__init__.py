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
    app.register_blueprint(api)


app = create_app()
db = MongoEngine(app)

# register
register_blueprints(app)

if __name__ == '__main__':
    app.run()
