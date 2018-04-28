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

        result = request.user.as_json(include_source=True)

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

        result = new_status.as_json()

        return un_chapeau_response(result)
