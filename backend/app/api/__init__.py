from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api', __name__)
api = Api(bp)


from .user import UserDetail, UserList
from .errors import exceptions
from .errors.handlers import error_response
from .auth import Login, Logout, LogoutAll


api.add_resource(
    UserDetail, '/users/<int:user_id>', endpoint='user_detail')
api.add_resource(UserList, '/users', endpoint='user_list')


api.add_resource(Login, '/auth/login', endpoint='auth_login')
api.add_resource(Logout, '/auth/logout', endpoint='auth_logout')
api.add_resource(LogoutAll, '/auth/logout/<int:user_id>',
                 endpoint='auth_logout_all')

bp.register_error_handler(exceptions.UsernameAlreadyUsed, error_response)
bp.register_error_handler(exceptions.EmailAddressAlreadyUsed, error_response)
bp.register_error_handler(
    exceptions.UserRequiredFieldsIsMissed, error_response)
bp.register_error_handler(exceptions.UserIdFieldIsMissed, error_response)
