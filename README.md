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
DEBUG:toot:>>> GET http://127.0.0.1:8999/api/v1/instance
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "GET /api/v1/instance HTTP/1.1" 200 245
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{\n  "contact_account": "marnanel",\n  "description": "just a test",\n  "email": "marnanel@thurman.org.uk",\n  "languages": [\n    "en_GB"\n  ],\n  "title": "un_chapeau test",\n  "uri": "http://127.0.0.1",\n  "urls": {},\n  "version": "un_chapeau 0.0.1"\n}'
DEBUG:toot:>>> POST http://127.0.0.1:8999/api/v1/apps
DEBUG:toot:>>> DATA:    {'client_name': 'toot - a Mastodon CLI client', 'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob', 'scopes': 'read write follow', 'website': 'https://github.com/ihabunek/toot'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "POST /api/v1/apps HTTP/1.1" 200 223
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{\n  "client_id": "Fz2DRhObvmTEj5ICxToxqqvTpUqlBLvJg5AnnEsZ",\n  "client_secret": "vTGPho6XPZlczDyKDaibBmQ7vNRurzg7yhOe9wtrRIGM5cusv99gBnkxIutK9jrdpcHhxgvT4F8dRVNknYamsVN830orTe2ZAnf4ZyGTMTKeMgigBB9NTOeI8W32vKRC",\n  "id": 4\n}'
Email:
```

Give it the email address and password you gave ```createsuperuser```.

```
DEBUG:toot:>>> POST http://127.0.0.1:8999/oauth/token
DEBUG:toot:>>> DATA:    {'grant_type': 'password', 'client_id': 'Fz2DRhObvmTEj5ICxToxqqvTpUqlBLvJg5AnnEsZ', 'username': 'you@example.com', 'scope': 'read write follow', 'password': 'lkx663plkx663p', 'client_secret': 'vTGPho6XPZlczDyKDaibBmQ7vNRurzg7yhOe9wtrRIGM5cusv99gBnkxIutK9jrdpcHhxgvT4F8dRVNknYamsVN830orTe2ZAnf4ZyGTMTKeMgigBB9NTOeI8W32vKRC'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "POST /oauth/token HTTP/1.1" 200 176
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{"token_type": "Bearer", "access_token": "Uo7SbUuqrLKlHcW9xDOSgHxQcAFqer", "refresh_token": "1IkFa21SmLDyMg4rtGla2TnWfhs8fD", "scope": "read write follow", "expires_in": 36000}'
DEBUG:toot:>>> GET http://127.0.0.1:8999/api/v1/accounts/verify_credentials
DEBUG:toot:>>> HEADERS: {'Authorization': 'Bearer Uo7SbUuqrLKlHcW9xDOSgHxQcAFqer'}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 127.0.0.1
DEBUG:urllib3.connectionpool:http://127.0.0.1:8999 "GET /api/v1/accounts/verify_credentials HTTP/1.1" 200 620
DEBUG:toot:<<< <Response [200]>
DEBUG:toot:<<< b'{\n  "acct": "marnanel",\n  "avatar": "https://marnanel.org/pics/un_chapeau_userpic_120.jpg",\n  "avatar_static": "https://marnanel.org/pics/un_chapeau_userpic_120.jpg",\n  "created_at": "2018-04-21T23:16:55.156258+00:00Z",\n  "display_name": "",\n  "followers_count": 0,\n  "following_count": 0,\n  "header": "https://marnanel.org/pics/un_chapeau_header_700.jpg",\n  "header_static": "https://marnanel.org/pics/un_chapeau_header_700.jpg",\n  "id": 1,\n  "locked": false,\n  "note": "",\n  "source": {\n    "note": "",\n    "privacy": "public",\n    "sensitive": false\n  },\n  "statuses_count": 0,\n  "url": "",\n  "username": "marnanel"\n}'
```

and you're logged in. You can't actually do anything until we implement some more, but at least you're logged in.

If you want to reset toot later, you must remove your server's entry in ```~/.config/toot/config.json```, under ```"apps"```.

See also
========

* [Mastodon API reference](https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md#account)
