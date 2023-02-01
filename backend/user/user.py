import uuid

from flask import Blueprint, request, make_response, send_file
import json

user = Blueprint('user', __name__)


@user.route('/user/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    if data['name'] == 'admin' and data['password'] == 'admin':
        return {
            'code': 200,
            'msg': '登录成功'
        }
    else:
        return {
            'code': 201,
            'msg': '登录失败'
        }


@user.route('/user/userInfo')
def user_info():
    username = request.args['userName']
    return {
        'name': username,
        'age': 18,
        'token': uuid.uuid1().hex
    }
