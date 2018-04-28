*un_chapeau* is a server for the Mastodon protocol, implemented in Django.

It's currently a long way from being useable.

How to get started
==================

* Clone this repository.
* `python setup.py migrate`
* `python setup.py createsuperuser`
* Make sure that whatever name you're using for the development server is ```listed in un_chapeau/un_chapeau/settings.py```
  under ```ALLOWED_HOSTS```, even if it's only ```"localhost"```.
* `python setup.py test`
* `python setup.py runserver 0.0.0.0:8999 &`

What works
==========

* Logging in via OAuth2.
* Posting a status.

For what's left to do, please see [the TODO list](TODO.md).

How to use toot
===============

Most Mastodon clients work only over HTTPS. Django's debugging server serves only HTTP. So
in case you want to use an actual client, rather than the test suite, I've
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

If you want to reset toot, you must remove your server's entry in ```~/.config/toot/config.json```, under ```"apps"```.

See also
========

* [Mastodon API reference](https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md#account)

Licence
=======

GNU AGPL.

