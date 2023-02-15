import json

from flask import request, jsonify, make_response, Blueprint

from service.user_service import create_user, login_user
from utils.logger import logger, accounts_logger

auth_view = Blueprint('auth', import_name=__name__)


@auth_view.route('/user/register', methods=['POST'])
def register():
    try:
        req_data = json.loads(request.data)
        user_name = req_data.get('login')
        first_name = req_data.get('first_name')
        last_name = req_data.get('last_name')
        password = req_data.get('password')
        data = create_user(user_name, first_name, last_name, password)
        return 'Success', 200
    except Exception as ex:
        accounts_logger.error(f'Failed to register with exception')
        accounts_logger.exception(ex)
        return jsonify(str(ex)), 400


@auth_view.route('/user/login', methods=['POST'])
def login():
    """
    Expects req data to be dict with login and password
    :return:
    """
    req_data = json.loads(request.data)
    user_name = req_data.get('login')
    password = req_data.get('password')
    try:
        token = login_user(user_name, password)
        # return data, status=default 200, headers= default empty
        return jsonify(dict(token=token.token)), 200
    except Exception as ex:
        return jsonify(str(ex)), 401
