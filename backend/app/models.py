from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True,
                         nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    session_id = db.relationship('Session', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


@event.listens_for(User, 'before_update')
@event.listens_for(User, 'before_insert')
def update_password_hash(mapper, connection, target):
    if target.password is not None:
        target.set_password(target.password)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip = db.Column(db.String(40))
    os = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    token = db.Column(db.String(100), index=True, unique=True)
    expired_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Session {self.id}>'
