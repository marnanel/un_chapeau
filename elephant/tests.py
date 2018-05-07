from django.test import TestCase, Client
from elephant.models import *

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

HTTP_AUTH = 'HTTP_AUTHORIZATION'

EXPECTED_CONTENT_TYPE = 'expected_content_type'
DEFAULT_EXPECTED_CONTENT_TYPE = 'application/json'

EXPECTED_STATUS_CODE = 'expected_status_code'
DEFAULT_EXPECTED_STATUS_CODE = 200

class UnChapeauClient(Client):
    """
    Like an ordinary django.test.Client, except that:

    - you can set 'authorization' to be an authorization string,
        and it will be used in all future requests

    - requests can have 'expected_content_type' and
        'expected_status_code' parameters
        """

    def __init__(self, **kwargs):
        super().__init__(kwargs)

        self.authorization = None

    def request(self, **request):

        """
        As the superclass, except for two more optional
        parameters:

        - expected_status_code causes ValueError if the
            code doesn't match; None disables the check;
            the default is 200.

        - expected_content_type causes ValueError if the
            Content-Type doesn't match; None disables the check;
            the default is 'application/json'.

        """

        if self.authorization is not None and HTTP_AUTH not in request:
            request[HTTP_AUTH] = self.authorization

        result = super().request(**request)

        expected_status_code = request.get(EXPECTED_STATUS_CODE,
                DEFAULT_EXPECTED_STATUS_CODE)
        expected_content_type = request.get(EXPECTED_CONTENT_TYPE,
                DEFAULT_EXPECTED_CONTENT_TYPE)

        # XXX These should really be assertions, but
        # XXX we don't have the TestCase object here. FIXME

        if expected_status_code is not None:
            if result.status_code != expected_status_code:
                raise ValueError('status code: expected %d, got %d: %s' % (
                    expected_status_code, result.status_code,
                    str(result.content)))
        elif expected_content_type is not None:
            if result['Content-Type'] != expected_content_type:
                raise ValueError('Content-Type: expected %s, got %s: %s' % (
                    expected_content_type, result['Content-Type'],
                    str(result.content)))

        return result

    def login(self):

        self.app = self.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS

        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'], # username is the email
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = self.app[key]

        self.token = self.post('/oauth/token', token_params).json()

        self.authorization = 'Bearer '+self.token['access_token']

class UnChapeauTestCase(TestCase):
    def _createFred(self):
        self.user_fred = User.objects.create_user(
                username='fred',
                email='fred@example.com',
                password='fredfred')

    def _createJim(self):
        user_jim = User.objects.create_user(
                username='jim',
                email='jim@example.com',
                password='jimjim')

class AuthTests(UnChapeauTestCase):
    def test_create_app(self):
        c = UnChapeauClient()

        app = c.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        for key in ['client_id', 'client_secret', 'id']:
            self.assertIn(key, app)

    def test_create_token(self):
        c = UnChapeauClient()

        app = c.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = c.post('/oauth/token', TOKEN_REQUEST_PARAMS).json()

        for key in ['access_token','token_type','scope']:
            self.assertIn(key, token)

        self.assertEqual(token['scope'], token_params['scope'])
        self.assertEqual(token['token_type'].lower(), 'bearer')

    def test_create_token_fails(self):
        c = UnChapeauClient()

        app = c.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS
        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        # add an "x" so we know it's not the real code
        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key] + 'x'

        token = c.post('/oauth/token',
                TOKEN_REQUEST_PARAMS,
                expected_status_code = 401)

    def test_login(self):
        c = UnChapeauClient()

        app = c.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS

        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = c.post('/oauth/token', token_params).json()

        c.authorization = 'Bearer '+token['access_token']

        account = c.get('/api/v1/accounts/verify_credentials').json()

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

        app = c.post('/api/v1/apps', APPS_CREATE_PARAMS).json()

        token_params = TOKEN_REQUEST_PARAMS

        self.user = User.objects.create_user(
                username=token_params['username'],
                email=token_params['username'],
                password=token_params['password'])

        for key in ['client_id', 'client_secret']:
            token_params[key] = app[key]

        token = c.post('/oauth/token', token_params).json()

        c.authorization = 'Bearer '+token['access_token']+'x'

        account = c.get('/api/v1/accounts/verify_credentials',

                # Error pages are text/html at present, for debugging;
                # this is wrong, because they should be application/json,
                # but we'll fix it when we reasonably can.
                expected_content_type = 'text/html',

                expected_status_code = 401)

    def test_client_login_method(self):
        c = UnChapeauClient()

        c.login()

class StatusTests(UnChapeauTestCase):

    def test_post_status(self):
        c = UnChapeauClient()

        c.login()

        status_params = {
                'status': 'Hello world!',
                }
        status = c.post('/api/v1/statuses', status_params,
                expected_status_code = 201).json()

        for key in [
                'id', 'uri', 'url', 'account', 'content',
                'created_at', 'emojis', 'reblogs_count',
                'favourites_count', 'sensitive',
                'spoiler_text', 'visibility',
                'media_attachments',
                'mentions', 'tags']:
                self.assertIn(key, status)

    def test_sensitive_status(self):
        self._createFred()

        for sensitive_by_default in (False, True):

            if sensitive_by_default:
                self.user_fred.default_sensitive = True

            ordinary_status = Status.objects.create(
                posted_by = self.user_fred,
                status = 'I like cheese. It is delicious.',
                )

            self.assertEqual(ordinary_status.is_sensitive(),
                    sensitive_by_default)

            nsfw_status = Status.objects.create(
                posted_by = self.user_fred,
                status = 'I was very naughty today.',
                sensitive = True,
                )

            self.assertEqual(nsfw_status.is_sensitive(), True)

            spoiler_status = Status.objects.create(
                posted_by = self.user_fred,
                spoiler_text = 'Spoilers for Jekyll and Hyde',
                status = 'They turn out to be the same guy.',
                )

            self.assertEqual(spoiler_status.is_sensitive(), True)

            nsfw_spoiler_status = Status.objects.create(
                posted_by = self.user_fred,
                sensitive = True,
                spoiler_text = 'Lex Luthor being naughty.',
                status = 'He stole 40 cakes.',
                )

            self.assertEqual(nsfw_spoiler_status.is_sensitive(), True)

class UserTests(UnChapeauTestCase):

    def test_status_count(self):
        self._createFred()

        self.assertEqual(self.user_fred.statuses_count(), 0)

        for i in range(1, 13):
            Status.objects.create(
                    status= 'Hello world!',
                    posted_by = self.user_fred,
                    )
            self.assertEqual(self.user_fred.statuses_count(), i)

class TimelineTests(UnChapeauTestCase):

    CREATE_COUNT = 20

    def test_public_timeline(self):
        self._createFred()

        statuses = []
        for i in range(self.CREATE_COUNT):
            statuses.append(Status.objects.create(
                    status = 'Hello %04d!' % (i,),
                    posted_by = self.user_fred,
                    ))

        c = UnChapeauClient()

        timeline = c.get('/api/v1/timelines/public').json()

        self.assertEqual(len(timeline), len(statuses))

        for i, status in enumerate(statuses):
            self.assertEqual(status.content,
                    timeline[i]['content'])
