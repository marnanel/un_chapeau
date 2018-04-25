from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from oauth2_provider.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Status
import json

def un_chapeau_response(d):
    return HttpResponse(
            content_type = 'application/json',
            content = json.dumps(d, indent=2, sort_keys=True),
            status = 200,
            reason = 'love and hugs',
            charset = 'UTF-8')

def iso_date(date):
    return date.isoformat()+'Z'

###########################

class Instance(View):

    def get(self, request, *args, **kwargs):

        result = {
            'uri': 'http://127.0.0.1',
            'title': 'un_chapeau test',
            'description': 'just a test',
            'email': 'marnanel@thurman.org.uk',
            'version': 'un_chapeau 0.0.1',
            'urls': {},
            'languages': ['en_GB'],
            'contact_account': 'marnanel',
            }

        return un_chapeau_response(result)

###########################

class Apps(View):

    def post(self, request, *args, **kwargs):

        new_app = Application(
            name = request.POST['client_name'],
            redirect_uris = request.POST['redirect_uris'],
            client_type = 'confidential', # ?
            authorization_grant_type = 'password',
            user = None, # don't need to be logged in
            )

        new_app.save()

        result = {
            'id': new_app.id,
            'client_id': new_app.client_id,
            'client_secret': new_app.client_secret,
            }

        return un_chapeau_response(result)

class Verify_Credentials(LoginRequiredMixin, View):

    raise_exception = True # 403 if they're not authenticated

    def get(self, request, *args, **kwargs):

        user = request.user

        result = {
            'id': user.id,
            'username': user.username,
            'acct': user.username, # XXX for remote ones we need to split this up
            'display_name': user.display_name,
            'locked': user.is_locked,
            'created_at': iso_date(user.created_at),
            'note': user.note,
            'url': user.url,
            'avatar': '/static/un_chapeau/defaults/avatar_1.jpg',
            'avatar_static': '/static/un_chapeau/defaults/avatar_1.jpg',
            'header': '/static/un_chapeau/defaults/header.jpg',
            'header_static': '/static/un_chapeau/defaults/header.jpg',
            'followers_count': 0,
            'following_count': 0,
            'statuses_count': 0,
            'source': {
                'privacy': 'public',
                'sensitive': False,
                'note': user.note,
                },
            }

        return un_chapeau_response(result)

class Statuses(View):

    def post(self, request, *args, **kwargs):
        # XXX require authentication here

        new_status = Status(
            content = request.POST['status'],
            #sensitive = int(request.POST['sensitive']),
            #spoiler_text = request.POST['spoiler_text'],
            visibility = request.POST['visibility'],

            # XXX we can't do media IDs until we implement media
            # XXX idempotency taken from "Idempotency-Key" header
            # XXX sanitise HTML

            )

        new_status.save()

        # XXX obviously this will need splitting out
        result = {
                "id": new_status.id,
                "uri": "?",
                "url": "?",
                "account": "your account",
                "content": new_status.content,
                'created_at': iso_date(new_status.created_at),
                "emojis": [],
                "reblogs_count": 0,
                "favourites_count": 0,
                "reblogged": False,
                "favourited": False,
                "muted": False,
                "sensitive": new_status.is_sensitive(),
                "spoiler_text": new_status.spoiler_text,
                "visibility": new_status.visibility,
                "media_attachments": [],
                "mentions": [],
                "tags": [],
                "language": '', # XXX null?
                "pinned": False,
            }

        return un_chapeau_response(result)
