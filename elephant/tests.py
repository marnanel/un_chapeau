from django.test import TestCase, Client
from elephant.models import User

# Create your tests here.

APPS_CREATE_PARAMS = {
        'client_name': 'un_chapeau tests',
        'scopes': 'read write follow',
        'website': 'http://example.com',
        'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
        }

TOKEN_REQUEST_PARAMS = {
        'client_secret': '',
        'client_id': '',
        'grant_type': 'password',
        'username': 'fred@example.com',
        'password': 'i_like_bananas',
        'scope': 'read write follow',
        }

class AuthTests(TestCase):
    def test_create_app(self):
        c = Client()

        app = c.post('/api/v1/apps',
                APPS_CREATE_PARAMS).json()

        for key in ['client_id', 'client_secret', 'id']:
            self.assertIn(key, app)

    def test_create_token(self):
        c = Client()

        app = c.post('/api/v1/apps',
                APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = c.post('/oauth/token',
                TOKEN_REQUEST_PARAMS).json()

        for key in ['access_token','token_type','scope']:
            self.assertIn(key, token)

        self.assertEqual(token['scope'], token_params['scope'])
        self.assertEqual(token['token_type'].lower(), 'bearer')
