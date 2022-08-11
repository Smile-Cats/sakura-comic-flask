import datetime

from flask import current_app, jsonify
from ..extensions import auth
from authlib.jose import jwt, JoseError


def generate_auth_token(user_id, name, effective_time=30, **kwargs):
    """生成用于登录认证的JWT（json web token）, effective_time 生成的token的有效时长"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = current_app.config['SECRET_KEY']
    # 待签名的数据负载
    data = {'id': user_id, 'name': name,
            'dead_time': (datetime.datetime.now() + datetime.timedelta(days=effective_time)).strftime("%Y-%m-%d")}
    data.update(**kwargs)
    token = jwt.encode(header=header, payload=data, key=key)
    return token.decode()


def parse_user_from_token(token: str) -> dict:
    '''
    用于从token中解析用户信息
    :param token:
    :return:
    '''
    key = current_app.config['SECRET_KEY']
    data = dict(jwt.decode(token, key))
    return data


# 将验证token的函数加载到auth对象中
# 此后auth.login_required 方法每次都会调用此函数来验证token
@auth.verify_token
def validate_token(token):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    key = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(token, key)
        dead_time = data['dead_time']
        if datetime.datetime.strptime(dead_time, "%Y-%m-%d") > datetime.datetime.now():
            return True
        return False
    except JoseError:
        return False


@auth.error_handler
def error_handler():
    return jsonify(dict(data={'code': 401, 'message': '401 Unauthorized Access'}))