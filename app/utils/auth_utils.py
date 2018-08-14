import jwt
from functools import wraps
from flask import request, jsonify
from app.models import User
from app.settings import Config


def login_require_body(f, AuthCls, *args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return jsonify(message="Empty auth header", status=False, token=None), 401
    auth_token = auth_header.split(" ")
    if len(auth_token) <= 1:
        response = jsonify(
            message="Auth header invalid",
            status=False,
            token=None
        )
        return response, 401
    auth_token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        phonenum = payload.get('sub')
        auth_user = AuthCls.query.filter_by(phonenum=phonenum).first()
        if auth_user is None:
            response = jsonify(message="User does not exist", status=False, token=None)
            return response, 401
        else:
            if auth_user.token != auth_token:
                response = jsonify(
                    message="Token invalid",
                    status=False,
                    token=None
                )
                return response, 401
            else:
                request.user = auth_user
                return f(*args, **kwargs)
    except jwt.ExpiredSignatureError:
        response = jsonify(
            message="token过期",
            status=False,
            token=None
        )
        return response, 401
    except jwt.DecodeError:
        response = jsonify(message="token不合法", status=False, token=None)
        return response, 401


def login_required(f):
    AuthCls = User

    @wraps(f)
    def wrap(*args, **kwargs):
        return login_require_body(f, AuthCls, *args, **kwargs)

    return wrap
