import IP
from flask import Blueprint, request, render_template, jsonify

weather = Blueprint('weather', __name__, url_prefix='/weather')


@weather.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    location = IP.find(ip)
    return jsonify(location=location, ip=ip)
