import IP
from flask import Blueprint, request, render_template, jsonify

weather = Blueprint('weather', __name__, url_prefix='/weather')


@weather.route('/', methods=['GET'])
def index():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remotw_addr
    location = IP.find(ip)
    return jsonify(location=location, ip=ip)
