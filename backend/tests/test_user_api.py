import json
import unittest
from base64 import b64encode

from flask_restful import url_for

from app import create_app, db
from app.models import User
from app.config import Config
from app.schemas import user_schema, users_schema
from app.api.errors import exceptions
from .utils import make_basic_auth_headers, make_token_auth_headers


class UserAPITestCase(unittest.TestCase):
    def setUp(self):

        self.maxDiff = None
        self.app = create_app(Config)
        self.app_context = self.app.test_request_context()
        self.app_context.push()

        db.drop_all()

        db.create_all()
        self.client = self.app.test_client()
        self.test_password = 'test_password'

        self.user_data = {'username': 'user100',
                          'password': self.test_password,
                          'email': 'user100@example.com'}

        self.user1 = User(username='john', email='john@example.com',
                          password=self.test_password)
        self.user2 = User(username='Siri', email='siri@example.com',
                          password=self.test_password)

        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        self.updated_user_data = {'username': 'user100',
                                  'email': 'user100@example.com'}

        self.user1_BAH = make_basic_auth_headers(
            self.user1.username, self.test_password)
        self.user2_BAH = make_basic_auth_headers(
            self.user2.username, self.test_password)

        response = self.client.post(
            url_for('api.auth_login'), headers=self.user1_BAH)
        access_token = json.loads(response.data)['access_token']
        self.user1_token_auth_headers = make_token_auth_headers(access_token)

        response = self.client.post(
            url_for('api.auth_login'), headers=self.user2_BAH)
        access_token = json.loads(response.data)['access_token']
        self.user2_token_auth_headers = make_token_auth_headers(access_token)

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        response = self.client.post(
            url_for('api.user_list'),
            data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        new_user = User.query.filter_by(
            username=self.user_data['username']).first()
        self.assertEqual(
            response.headers['Location'],
            url_for('api.user_detail', user_id=new_user.id, _external=True))
        data = json.loads(response.data)
        self.assertIn('email', data)
        self.assertIn('username', data)
        self.assertIn('id', data)
        self.assertEqual(data['username'], self.user_data['username'])
        self.assertEqual(data['id'], new_user.id)
        self.assertTrue(new_user.check_password(self.user_data['password']))
        self.assertEqual(new_user.email, self.user_data['email'])

    def test_create_user_error_on_incomplete_data(self):
        for key in self.user_data.keys():
            user_data = self.user_data.copy()
            user_data.pop(key, None)
            response = self.client.post(
                url_for('api.user_list'), data=json.dumps(user_data),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_create_user_error_on_blank_required_field(self):
        for key in self.user_data.keys():
            user_data = self.user_data.copy()
            user_data[key] = ''
            response = self.client.post(
                url_for('api.user_list'), data=json.dumps(user_data),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_create_user_error_on_none_required_field(self):
        for key in self.user_data.keys():
            user_data = self.user_data.copy()
            user_data[key] = None
            response = self.client.post(
                url_for('api.user_list'), data=json.dumps(user_data),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_create_user_error_on_unknown_field(self):
        user_data = self.user_data.copy()
        user_data['custom_field'] = 'Blabla'
        response = self.client.post(
            url_for('api.user_list'), data=json.dumps(user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_error_on_username_already_used(self):
        self.user_data['username'] = self.user1.username
        response = self.client.post(
            url_for('api.user_list'), data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(exceptions.UsernameAlreadyUsed.description,
                      str(response.data))

    def test_create_user_error_on_email_already_used(self):
        self.user_data['email'] = self.user1.email
        response = self.client.post(
            url_for('api.user_list'), data=json.dumps(self.user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(exceptions.EmailAddressAlreadyUsed.description,
                      str(response.data))

    def test_get_users(self):
        response = self.client.get(
            url_for('api.user_list'), headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        data1 = users_schema.dump(User.query.all())
        self.assertEqual(data, data1)
        self.assertEqual(len(data), 2)
        self.assertIn(user_schema.dump(self.user1), data)
        self.assertIn(user_schema.dump(self.user2), data)

    def test_get_users_token_auth_required(self):
        response = self.client.get(url_for('api.user_list'), headers={})
        self.assertEqual(response.status_code, 401)
        response = self.client.get(
            url_for('api.user_list'), headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        response = self.client.get(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 200)
        data = user_schema.dump(User.query.get(self.user1.id))
        self.assertEqual(json.loads(response.data), data)

    def test_get_user_token_auth_required(self):
        response = self.client.get(
            url_for('api.user_detail', user_id=self.user1.id))
        self.assertEqual(response.status_code, 401)
        response = self.client.get(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_user_does_not_exists(self):
        response = self.client.get(
            url_for('api.user_detail', user_id=100),
            headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps(self.updated_user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['username'], self.updated_user_data['username'])
        self.assertEqual(
            self.user1.email, self.updated_user_data['email'])

    def test_update_user_with_password(self):
        updated_data = self.updated_user_data.copy()
        updated_data['password'] = 'test_password2'
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps(updated_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['username'], self.updated_user_data['username'])
        self.assertTrue(self.user1.check_password(updated_data['password']))
        self.assertEqual(
            self.user1.email, self.updated_user_data['email'])

    def test_update_user_error_on_not_self_update(self):
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user2.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps(self.updated_user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps(self.updated_user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_user_on_user_name_already_used(self):
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps({'username': self.user2.username}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(exceptions.UsernameAlreadyUsed.description,
                      str(response.data))
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps({'username': 'user100'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_user_on_email_already_used(self):
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps({'email': self.user2.email}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(exceptions.EmailAddressAlreadyUsed.description,
                      str(response.data))
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps({'email': 'user100@example.com'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_user_token_auth_required(self):
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers={},
            data=json.dumps(self.updated_user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        response = self.client.put(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers,
            data=json.dumps(self.updated_user_data),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            url_for('api.user_detail', user_id=self.user1.id),
            headers=self.user2_token_auth_headers)
        self.assertEqual(response.status_code, 404)

    def tets_delete_error_on_not_self_deletion(self):
        response = self.client.delete(
            url_for('api.user_detail', user_id=self.user2.id),
            headers=self.user1_token_auth_headers)
        self.assertEqual(response.status_code, 401)

    def test_delete_user_token_auth_required(self):
        response = self.client.delete(
            url_for('api.user_detail', user_id=self.user1.id))
        self.assertEqual(response.status_code, 401)
