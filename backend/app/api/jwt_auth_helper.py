from datetime import datetime
from functools import wraps
from secrets import token_urlsafe

import jwt
from flask import abort, current_app, request, g
from werkzeug import UserAgent
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models import Session


def _is_rt_expired(payload, now=None):
    expiration_date = datetime.utcfromtimestamp(payload['rt_expiration'])
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


def revoke_refresh_token(token):
    session = Session.query.filter(Session.token == token).first()
    db.session.delete(session)
    db.session.commit()
    expires_delta = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 0)
    revoke_token(token, expires_delta)


def revoke_all_refresh_tokens(user_id):
    sessions = Session.query.filter(Session.user_id == user_id)
    expires_delta = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    for session in sessions:
        revoke_token(session.token, expires_delta)
        db.session.delete(session)
    db.session.commit()


def create_session(now=None, expires_delta=None):
    now = datetime.utcnow() if not now else now
    if not expires_delta:
        expires_delta = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    rt = token_urlsafe(32)
    rt_expiration = now + expires_delta
    user_agent = request.headers.get('User-Agent')
    os = UserAgent(user_agent).platform
    session = Session(user_id=g.current_user_id, ip=request.remote_addr, os=os,
                      user_agent=request.headers.get('User-Agent'), token=rt,
                      expired_at=rt_expiration, created_at=now, updated_at=now)
    current_app.redis.set(rt, 'false', expires_delta)
    db.session.add(session)
    db.session.commit()
    return session


def make_payload(session):
    payload = {
        'user_id': g.current_user_id,
        'refresh_token': session.token,
        'rt_expiration': session.expired_at.timestamp(),
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


def _touch_refresh_token(payload, now=datetime.utcnow()):
    try:
        rt_expiration = now + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        current_session = Session.query.filter(
            Session.user_id == payload['user_id'],
            Session.token == payload['refresh_token'],
            Session.expired_at > now).one()
        current_session.expired_at = rt_expiration
        db.session.add(current_session)
        db.session.commit()
        return rt_expiration
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

        if _is_rt_expired(payload, now):
            abort(401)
        if _is_token_revoked(payload['refresh_token']):
            abort(401)
        if _is_user_agent_changed(payload):
            abort(401)
        if _is_os_changed(payload):
            abort(401)

        if _is_at_expired(payload, now):
            rt_expiration = _touch_refresh_token(payload, now=now)
            payload['rt_expiration'] = rt_expiration.timestamp()
            g.new_access_token = create_access_token(payload)
            return fn(*args, **kwargs)

        rt_expiration = _touch_refresh_token(payload, now=now)
        payload['rt_expiration'] = rt_expiration.timestamp()
        g.new_access_token = create_access_token(payload)
        return fn(*args, **kwargs)

    return wrapper
