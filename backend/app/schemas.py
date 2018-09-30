from marshmallow import fields, Schema, validates, RAISE
from marshmallow.validate import Length

from app.models import User


class UserSchema(Schema):
    class Meta:
        unknown = RAISE
    id = fields.Int(dump_only=True)
    username = fields.Str(
        64, required=True, allow_none=False, validate=Length(min=1))
    email = fields.Email(120, required=True, allow_none=False)
    password = fields.Str(required=True, load_only=True,
                          validate=Length(min=1))
    token = fields.Str(load_only=True)
    token_expiration = fields.DateTime(load_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
