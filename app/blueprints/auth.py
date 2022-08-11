from flask import Blueprint, request, jsonify, Response, url_for
from ..extensions import db, auth
from ..utils.auth_verify_util import generate_auth_token, parse_user_from_token
from ..models.models import *

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    json_data = request.json
    if not json_data:
        return jsonify(data={
            'code': 400,
            'message': '请输入账户和密码'
        })
    name = json_data.get('name', None)
    password = json_data.get('password', None)
    if name and password:
        user = User.query.filter_by(name=name).first()  # 查找user表中第一个数据
        if user:
            if name == user.name and user.validate_password(password):
                token = generate_auth_token(user_id=user.id, name=name, effective_time=30)
                print(token)
                return jsonify(data={
                    'code': 200,
                    'message': 'Login successfully',
                    'token': 'jwt ' + token
                })
    return jsonify(data={
                    'code': 400,
                    'message': '登录失败, 账户或密码不正确'
                })


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    json_data = request.json
    if not json_data:
        return jsonify(data={
            'code': 400,
            'message': '请输入账户和密码'
        })
    name = json_data.get('name', None)
    password = json_data.get('password', None)
    if name and password:
        user = User.query.filter_by(name=name).first()  # 查找user表中是否有此用户名
        if user:
            return jsonify(data={
                'code': 400,
                'message': '注册失败, 当前用户名已被注册, 请更换用户名'
            })
        else:
            user = User(name=name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify(data={
                'code': 200,
                'message': '注册成功, 请重新登录'
            })
    return jsonify(data={
                'code': 400,
                'message': '注册失败, 账户或密码未填写'
            }
    )


@auth_bp.route('/auth/user', methods=['GET'])
@auth.login_required
def get_user():
    jwt_token = request.headers['Authorization'].split(' ')[-1]
    user_dict = parse_user_from_token(jwt_token)
    return jsonify(data={
                'code': 200,
                'message': '获取用户信息成功',
                'data': user_dict
            }
    )




@auth_bp.route('/api/check')
@auth.login_required
def check_token():
    print(request.headers)
    return jsonify(data={
        'message': 'scuess'
    })
