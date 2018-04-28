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

class UnChapeauClient(Client):

    http_auth = 'HTTP_AUTHORIZATION'

    def __init__(self, **kwargs):
        super().__init__(kwargs)

        self.authorization = None

    def request(self, **request):

        if self.authorization is not None and http_auth not in request:
            request[http_auth] = self.authorization

        result = super().request(**request)

        return result

class UnChapeauTestCase(TestCase):

    def _get_json(self, response):
        self.assertEqual(response.status_code, 200,
                msg=str(response.content))
        self.assertEqual(response['Content-Type'], 'application/json',
                msg=str(response.content))
        return response.json()

    def assertHttpFailCode(self, response,
            failcode):
        self.assertEqual(response.status_code, failcode,
                msg=str(response.content))

    def login(self):
        c = UnChapeauClient()

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
                HTTP_AUTHORIZATION = 'Bearer '+token['access_token']))



class AuthTests(UnChapeauTestCase):
    def test_create_app(self):
        c = UnChapeauClient()

        app = self._get_json(c.post('/api/v1/apps',
                APPS_CREATE_PARAMS))

        for key in ['client_id', 'client_secret', 'id']:
            self.assertIn(key, app)

    def test_create_token(self):
        c = UnChapeauClient()

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
        c = UnChapeauClient()

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

        self.assertHttpFailCode(token, 401)

    def test_login(self):
        c = UnChapeauClient()

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
                HTTP_AUTHORIZATION = 'Bearer '+token['access_token']))

        for key in ['id', 'username', 'acct', 'display_name',
                'locked', 'created_at', 'note', 'avatar',
                'avatar_static', 'header', 'header_static',
                'followers_count', 'following_count',
                'source']:
            self.assertIn(key, account)

        for key in ['privacy', 'sensitive', 'note']:
            self.assertIn(key, account['source'])

    def test_login_fails(self):
        c = UnChapeauClient()

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
                HTTP_AUTHORIZATION = 'Bearer '+token['access_token']+'x')

        self.assertHttpFailCode(account, 403)
        
