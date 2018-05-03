from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from oauth2_provider.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from un_chapeau.settings import UN_CHAPEAU_SETTINGS
from .models import Status
import json

###########################

class Instance(View):

    def get(self, request, *args, **kwargs):

        result = {
            'uri': 'http://127.0.0.1',
            'title': UN_CHAPEAU_SETTINGS['INSTANCE_NAME'],
            'description': UN_CHAPEAU_SETTINGS['INSTANCE_DESCRIPTION'],
            'email': UN_CHAPEAU_SETTINGS['CONTACT_EMAIL'],
            'version': 'un_chapeau 0.0.1',
            'urls': {},
            'languages': UN_CHAPEAU_SETTINGS['LANGUAGES'],
            'contact_account': UN_CHAPEAU_SETTINGS['CONTACT_ACCOUNT'],
            }

        return JsonResponse(result)

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

        return JsonResponse(result)

class Verify_Credentials(LoginRequiredMixin, View):

    raise_exception = True # 403 if they're not authenticated

    def get(self, request, *args, **kwargs):

        result = request.user.as_json(include_source=True)

        return JsonResponse(result)

class Statuses(View):

    def post(self, request, *args, **kwargs):
        # XXX require authentication here

        new_status = Status(
            content = request.POST['status'],
            #sensitive = int(request.POST['sensitive']),
            #spoiler_text = request.POST['spoiler_text'],
            visibility = request.POST.get('visibility', 'public'),

            # XXX we can't do media IDs until we implement media
            # XXX idempotency taken from "Idempotency-Key" header
            # XXX sanitise HTML

            )

        new_status.save()

        result = new_status.as_json()

        return JsonResponse(result)
