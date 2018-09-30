from werkzeug.exceptions import BadRequest


class UserIdFieldIsMissed(BadRequest):
    description = 'must include user_id field'


class UsernameAlreadyUsed(BadRequest):
    description = 'please use a different username'


class EmailAddressAlreadyUsed(BadRequest):
    description = 'please use a different email address'


class UserRequiredFieldsIsMissed(BadRequest):
    description = 'must include username, email and password fields'
