import json
import unittest
from datetime import datetime

from flask import current_app, g
from flask_restful import url_for

from app import create_app, db
from app.models import User, Session
from app.config import Config
from .utils import make_basic_auth_headers, make_token_auth_headers
from app.api.jwt_auth_helper import decode_token


class AuthAPITestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.app = create_app(Config)
        self.app_context = self.app.test_request_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

        self.test_password = 'test_password'
        self.user1 = User(username='john', email='john@example.com',
                          password=self.test_password)
        self.user2 = User(username='Siri', email='siri@example.com',
                          password=self.test_password)

        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        self.user1_BAH = make_basic_auth_headers(self.user1.username,
                                                 self.test_password)
        response = self.client.post(url_for('api.auth_login'),
                                    headers=self.user1_BAH)
        self.user1_at = json.loads(response.data)['access_token']
        self.user1_TAH = make_token_auth_headers(self.user1_at)

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        now = datetime.utcnow()
        response = self.client.post(url_for('api.auth_login'),
                                    headers=self.user1_BAH)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        payload = decode_token(data['access_token'])

        session = Session.query.filter_by(
            token=payload['refresh_token']).first()
        self.assertIsNotNone(session)

        revoke_status = current_app.redis.get(session.token)
        self.assertIsNotNone(revoke_status)
        self.assertEqual(revoke_status.decode('utf-8'), 'false')

        self.assertIn('refresh_token', payload)
        self.assertIn('rt_expiration', payload)
        self.assertIn('os', payload)
        self.assertIn('user_agent', payload)
        self.assertIn('user_id', payload)
        self.assertIn('exp', payload)
        self.assertIn('ip', payload)

        rt_expiration = datetime.utcfromtimestamp(payload['rt_expiration'])
        rt_delta = rt_expiration - now
        at_expiration = datetime.utcfromtimestamp(payload['exp'])
        at_delta = at_expiration - now

        self.assertEqual(rt_delta.days,
                         Config.JWT_REFRESH_TOKEN_EXPIRES.days)
        self.assertGreater(Config.JWT_ACCESS_TOKEN_EXPIRES, at_delta)
        self.assertEqual(session.token, payload['refresh_token'])
        self.assertEqual(session.expired_at, rt_expiration)
        self.assertEqual(session.os, payload['os'])
        self.assertEqual(session.user_agent, payload['user_agent'])
        self.assertEqual(session.ip, payload['ip'])
        self.assertEqual(self.user1.id, payload['user_id'])
        self.assertIsNotNone(getattr(g, 'current_user_id'))
        self.assertEqual(g.current_user_id, self.user1.id,)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.delete(url_for('api.auth_logout'),
                                      headers=self.user1_TAH)
        payload = decode_token(self.user1_at)
        session = Session.query.filter_by(
            token=payload['refresh_token']).first()
        self.assertIsNone(session)
        revoke_status = current_app.redis.get(payload['refresh_token'])
        self.assertIsNotNone(revoke_status)
        self.assertEqual(revoke_status.decode('utf-8'), 'true')
        self.assertEqual(response.status_code, 200)

    def test_logout_all(self):
        response = self.client.delete(
            url_for('api.auth_logout_all', user_id=self.user1.id),
            headers=self.user1_TAH)

        self.assertEqual(response.status_code, 200)
