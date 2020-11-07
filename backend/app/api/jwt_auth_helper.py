from datetime import datetime
from functools import wraps
from secrets import token_urlsafe

import jwt
from flask import abort, current_app, request, g
from werkzeug.useragents import UserAgent
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models import Session


def _is_session_expired(payload, now=None):
    expiration_date = datetime.utcfromtimestamp(payload['session_exp'])
    return expiration_date <= (datetime.utcnow() if not now else now)


def _is_at_expired(payload, now=None):
    expiration_date = datetime.utcfromtimestamp(payload['exp'])
    return expiration_date > (datetime.utcnow() if not now else now)


def _is_user_agent_changed(payload):
    return payload['user_agent'] != request.headers.get('User-Agent')


def _is_os_changed(payload):
    current_os = UserAgent(request.headers.get('User-Agent')).platform
    return payload['os'] != current_os


def _is_token_revoked(token):
    entry = current_app.redis.get(token)
    if entry is None:
        return True
    return entry == 'true'


def revoke_token(token, expires_delta):
    current_app.redis.set(token, 'true', expires_delta)


def delete_session(token):
    session = Session.query.filter(Session.token == token).first()
    db.session.delete(session)
    db.session.commit()
    expires_delta = current_app.config.get('JWT_SESSION_EXPIRES', 0)
    revoke_token(token, expires_delta)


def delete_all_sessions(user_id):
    sessions = Session.query.filter(Session.user_id == user_id)
    expires_delta = current_app.config['JWT_SESSION_EXPIRES']
    for session in sessions:
        revoke_token(session.token, expires_delta)
        db.session.delete(session)
    db.session.commit()


def create_session(now=None, expires_delta=None, user_id=None):
    user_id = user_id if user_id else g.current_user_id
    now = datetime.utcnow() if not now else now
    expires_delta = expires_delta if expires_delta else current_app.config['JWT_SESSION_EXPIRES']
    token = token_urlsafe(32)
    session_exp = now + expires_delta
    user_agent = request.headers.get('User-Agent')
    os = UserAgent(user_agent).platform if user_agent else ''
    session = Session(user_id=user_id, ip=request.remote_addr, os=os,
                      user_agent=request.headers.get('User-Agent'),
                      token=token, expired_at=session_exp, created_at=now,
                      updated_at=now)
    current_app.redis.set(token, 'false', expires_delta)
    db.session.add(session)
    db.session.commit()
    return session


def make_payload(session):
    payload = {
        'user_id': session.user_id,
        'session_token': session.token,
        'session_exp': session.expired_at.timestamp(),
        'ip': session.ip,
        'os': session.os,
        'user_agent': session.user_agent
    }
    return payload


def create_access_token(payload, expires_delta=None):
    if not expires_delta:
        expires_delta = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    payload['exp'] = datetime.utcnow() + expires_delta
    at = jwt.encode(payload, current_app.config['SECRET_KEY'],
                    algorithm='HS256')
    return at.decode('utf-8')


def decode_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')


def _touch_session(payload, now=datetime.utcnow()):
    try:
        session_exp = now + current_app.config['JWT_SESSION_EXPIRES']
        current_session = Session.query.filter(
            Session.user_id == payload['user_id'],
            Session.token == payload['session_token'],
            Session.expired_at > now).one()
        current_session.expired_at = session_exp
        db.session.add(current_session)
        db.session.commit()
        return session_exp
    except NoResultFound:
        abort(401)


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        now = datetime.utcnow()
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            abort(401)
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        g.payload = payload.copy()
        g.current_user_id = g.payload['user_id']

        if _is_session_expired(payload, now):
            abort(401)
        if _is_token_revoked(payload['session_token']):
            abort(401)
        if _is_user_agent_changed(payload):
            abort(401)
        if _is_os_changed(payload):
            abort(401)

        if _is_at_expired(payload, now):
            session_exp = _touch_session(payload, now=now)
            payload['session_exp'] = session_exp.timestamp()
            g.new_access_token = create_access_token(payload)
            return fn(*args, **kwargs)

        session_exp = _touch_session(payload, now=now)
        payload['session_exp'] = session_exp.timestamp()
        g.new_access_token = create_access_token(payload)
        return fn(*args, **kwargs)

    return wrapper


def login(now=None, user_id=None):
    now = datetime.utcnow() if not now else now
    user_id = user_id if user_id else g.current_user_id
    at_expiration = now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    at = create_access_token(make_payload(create_session(now=now, user_id=user_id)))
    token_data = {
        'access_token': at,
        'at_expiration': at_expiration.isoformat()+'Z',
        'user_id': user_id
    }
    return token_data
