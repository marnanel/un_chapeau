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

class UnChapeauTestCase(TestCase):

    def _get_json(self, response):
        self.assertEqual(response.status_code, 200,
                msg=str(response.content))
        self.assertEqual(response['Content-Type'], 'application/json',
                msg=str(response.content))
        return response.json()

    def assertForbidden(self, response):
        self.assertEqual(response.status_code, 403,
                msg=str(response.content))

class AuthTests(UnChapeauTestCase):
    def test_create_app(self):
        c = Client()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        for key in ['client_id', 'client_secret', 'id']:
            self.assertIn(key, app)

    def test_create_token(self):
        c = Client()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = self._get_json(c.post('/oauth/token',
                TOKEN_REQUEST_PARAMS))

        for key in ['access_token','token_type','scope']:
            self.assertIn(key, token)

        self.assertEqual(token['scope'], token_params['scope'])
        self.assertEqual(token['token_type'].lower(), 'bearer')

    def test_create_token_fails(self):
        c = Client()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key] + 'x'

        token = c.post('/oauth/token',
                TOKEN_REQUEST_PARAMS)

        self.assertForbidden(token)

    def test_login(self):
        c = Client()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = self._get_json(c.post('/oauth/token',
                token_params))

        account = self._get_json(c.get('/api/v1/accounts/verify_credentials',
                http_authorization = 'bearer '+token['access_token']))

        for key in ['id', 'username', 'acct', 'display_name',
                'locked', 'created_at', 'note', 'avatar',
                'avatar_static', 'header', 'header_static',
                'followers_count', 'following_count',
                'source']:
            self.assertin(key, account)

        for key in ['privacy', 'sensitive', 'note']:
            self.assertin(key, account['source'])

    def test_login_fails(self):
        c = Client()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = self._get_json(c.post('/oauth/token',
                token_params))

        account = c.get('/api/v1/accounts/verify_credentials',
                http_authorization = 'bearer '+token['access_token']+'x')

        self.assertForbidden(account)
