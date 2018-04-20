*un_chapeau* is a server for the Mastodon protocol, implemented in Django.

It's currently a long way from being useable. However, you can get as far as logging in.

How to get started
==================

Set up httptoot
---------------
Firstly, most Mastodon clients work only over HTTPS. Django's debugging server serves only HTTP. So I've
[modified toot](https://github.com/marnanel/toot/tree/httptoot)
to support fetching over HTTP, with the `-I` (insecure) option.
[Until this is merged into trunk](https://github.com/ihabunek/toot/issues/56), grab it with

```shell
git clone https://github.com/marnanel/toot.git
cd toot
git checkout httptoot
python setup.py install
```

If you do `toot login --help` you should now see an `-I, --insecure` option.

Get un_chapeau running in the Django debug server
-------------------------------------------------

* Clone this repository.
* `python setup.py migrate`
* `python setup.py createsuperuser`
* Make sure that whatever name you're using for the development server is ```listed in un_chapeau/un_chapeau/settings.py```
  under ```ALLOWED_HOSTS```, even if it's only ```"localhost"```.
* `python setup.py runserver 0.0.0.0:8999 &`

Log in
------

* `toot login -I -i 127.0.0.1:8999 --debug`

And you should see something like:
```
Looking up instance info...
DEBUG:toot:>>> GET http://127.0.0.1:8999/api/v1/instance
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "GET /api/v1/instance HTTP/1.1" 200 245
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{\n  "contact_account": "marnanel",\n  "description": "just a test",\n
"email": "marnanel@thurman.org.uk",\n  "languages": [\n    "en_GB"\n  ],\n  "title": "un_chapeau test",\n
"uri": "http://127.0.0.1",\n  "urls": {},\n  "version": "un_chapeau 0.0.1"\n}'
Found instance un_chapeau test running Mastodon version un_chapeau 0.0.1
Registering application...
DEBUG:toot:>>> POST http://127.0.0.1:8999/api/v1/apps
DEBUG:toot:>>> DATA:    {'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob', 'scopes': 'read write follow',
'website': 'https://github.com/ihabunek/toot', 'client_name': 'toot - a Mastodon CLI client'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "POST /api/v1/apps HTTP/1.1" 200 223
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{\n  "client_id": "5LAw5aKzJVQ7Q28yEOkmCj5AA5FcFWnWN45sWmQ3",\n
"client_secret": "really long string",\n "id": 4\n}'
Application tokens saved.
Log in to 127.0.0.1:8999
Email:
```

Give it the username and password you gave ```createsuperuser```. Despite the prompt, don't use the email address.

```
Authenticating...
DEBUG:toot:>>> POST http://127.0.0.1:8999/oauth/token
DEBUG:toot:>>> DATA:    {'scope': 'read write follow', 'client_secret': 'really long string', 'password': 'whatever',
'grant_type': 'password', 'username': 'whatever', 'client_id': '5LAw5aKzJVQ7Q28yEOkmCj5AA5FcFWnWN45sWmQ3'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "POST /oauth/token HTTP/1.1" 200 176
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{"token_type": "Bearer", "scope": "read write follow", "refresh_token": "pJbCx94qyuzQMLQPsW4aL9B5fjrqXv",
"expires_in": 36000, "access_token": "FvrS6RDcNqDu2TwTM5SohmhSjcu2T6"}'
DEBUG:toot:>>> GET http://127.0.0.1:8999/api/v1/accounts/verify_credentials
DEBUG:toot:>>> HEADERS: {'Authorization': 'Bearer FvrS6RDcNqDu2TwTM5SohmhSjcu2T6'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "GET /api/v1/accounts/verify_credentials HTTP/1.1" 404 2637
DEBUG:toot:<<< <Response [404]>
```

and it will fall over. Construction continues-- but, as you see, we've managed to authenticate. If you go to ```http://127.0.0.1:8999/admin``` you'll
see that our login credentials have been recorded.

If you want to reset toot later, you must remove your server's entry in ```~/.config/toot/config.json```, under ```"apps"```.

See also
========

* [Mastodon API reference](https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md#account)
