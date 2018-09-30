from datetime import datetime

from flask import current_app, jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized

from app.models import User
from .jwt_auth_helper import (
    create_access_token, jwt_required, revoke_refresh_token,
    revoke_all_refresh_tokens, create_session, make_payload)


basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def veryfy_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user_id = user.id
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    raise Unauthorized


class Login(Resource):
    method_decorators = {
        'post': [basic_auth.login_required],
    }

    def post(self):
        now = datetime.utcnow()
        at_expiration = now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        at = create_access_token(make_payload(create_session(now)))
        response = jsonify({'access_token': at,
                            'at_expiration': at_expiration.isoformat(),
                            'user_id': g.current_user_id})
        response.status_code = 200
        return response


class Logout(Resource):
    method_decorators = {
        'delete': [jwt_required]
    }

    def delete(self):
        revoke_refresh_token(g.payload['refresh_token'])
        return 200


class LogoutAll(Resource):
    method_decorators = {
        'delete': [jwt_required]
    }

    def delete(self, user_id):
        revoke_all_refresh_tokens(user_id)
        return 200
