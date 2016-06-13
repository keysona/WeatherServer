from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def root():
    return 'api'
