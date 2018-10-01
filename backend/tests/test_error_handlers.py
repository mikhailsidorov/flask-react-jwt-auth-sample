import json
from unittest import TestCase
from unittest.mock import Mock

from werkzeug.http import HTTP_STATUS_CODES

from app import create_app
from app.api.errors.handlers import error_response
from app.config import Config


class ErrorHandlerTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.app = create_app(Config)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.error = Mock()
        self.error.status_code = 400
        self.error.description = 'Test error message'

    def tearDown(self):
        del self.error

    def test_error_response(self):
        response = error_response(self.error)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, self.error.status_code)
        self.assertEqual(data['message'], self.error.description)
        self.assertEqual(
            data['error'], HTTP_STATUS_CODES[self.error.status_code])

        self.error.status_code = 511
        response = error_response(self.error)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unknown error')
