from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from werkzeug.exceptions import Unauthorized

from app.models import User
from .jwt_auth_helper import jwt_required, delete_session, delete_all_sessions, login


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
        response = jsonify(login())
        response.status_code = 200
        return response


class Logout(Resource):
    method_decorators = {
        'delete': [jwt_required]
    }

    def delete(self):
        delete_session(g.payload['session_token'])
        return 200


class LogoutAll(Resource):
    method_decorators = {
        'delete': [jwt_required]
    }

    def delete(self, user_id):
        delete_all_sessions(user_id)
        return 200
