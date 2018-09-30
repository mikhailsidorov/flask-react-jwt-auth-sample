from datetime import datetime

from flask import jsonify, request, url_for, abort, g
from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from app import db
from app.models import User
from app.schemas import user_schema, users_schema
from .errors import exceptions
from .jwt_auth_helper import (jwt_required, create_access_token, create_session,
                              make_payload, revoke_all_refresh_tokens)
from .permissions import allows, CanUpdateProfile, CanDeleteProfile


class UserDetail(Resource):
    method_decorators = {
        'get': [jwt_required],
        'put': [allows.requires(CanUpdateProfile()), jwt_required],
        'delete': [allows.requires(CanDeleteProfile()), jwt_required]
    }

    def get(self, user_id):
        return user_schema.dump(User.query.get_or_404(user_id))

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        raw_data = request.get_json() or {}
        data = user_schema.load(raw_data, partial=True)
        if 'username' in data and \
            data['username'] != user.username and \
                User.query.filter_by(username=data['username']).first():
            raise exceptions.UsernameAlreadyUsed
        if 'email' in data and \
            data['email'] != user.email and \
                User.query.filter_by(email=data['email']).first():
            raise exceptions.EmailAddressAlreadyUsed
        user.update(**data)
        db.session.commit()

        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        revoke_all_refresh_tokens(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 200


class UserList(Resource):
    method_decorators = {
        'get': [jwt_required],
    }

    def get(self):
        all_users = User.query.all()
        return users_schema.dump(all_users)

    def post(self):
        try:
            data = user_schema.load(request.get_json() or {})
        except ValidationError as err:
            first_invalid_field = list(err.messages.keys())[0]
            message = err.messages[first_invalid_field]
            abort(400, f'{first_invalid_field}: {message}')
        if User.query.filter_by(username=data['username']).first():
            raise exceptions.UsernameAlreadyUsed
        if User.query.filter_by(email=data['email']).first():
            raise exceptions.EmailAddressAlreadyUsed

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        response = jsonify(user_schema.dump(user))
        response.status_code = 201
        response.headers['Location'] = url_for('api.user_detail',
                                               user_id=user.id)
        return response
