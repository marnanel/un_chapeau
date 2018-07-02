from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
from oauth2_provider.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import SuspiciousOperation
from un_chapeau.settings import UN_CHAPEAU_SETTINGS
from .models import Status, User, Visibility
from .serializers import *
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
import re

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

class Verify_Credentials(generics.GenericAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = UserSerializerWithSource(request.user)
        return Response(serializer.data)

class Statuses(generics.ListCreateAPIView):

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticated, )

class AbstractTimeline(generics.ListAPIView):

    serializer_class = StatusSerializer
    permission_classes = ()

    def get_queryset(self):
        raise RuntimeError("cannot query abstract timeline")

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset,
                many = True,
                context = {
                    'request': request,
                    })
        return Response(serializer.data)

class PublicTimeline(AbstractTimeline):

    def get_queryset(self):
        return Status.objects.filter(visibility=Visibility('public').name)

########################################

class UserFeed(View):

    def get(self, request, username, *args, **kwargs):

        user = get_object_or_404(User, username=username)
        statuses = Status.objects.filter(posted_by=user)

        context = {
                'user': user,
                'statuses': statuses,
                'server_name': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'hub_url': UN_CHAPEAU_SETTINGS['HUB'],
            }

        return render(
                request=request,
                template_name='account.atom.xml',
                context=context,
                content_type='application/atom+xml',
                )

########################################

class Webfinger(generics.GenericAPIView):
    """
    RFC7033 webfinger support.
    """

    serializer_class = WebfingerSerializer
    permission_classes = ()

    def get(self, request):

        try:
            user = request.GET['resource']
        except MultiValueDictKeyError:
            raise SuspiciousOperation('no resource for webfinger')

        # Generally, user resources should be prefaced with "acct:",
        # per RFC7565. We support this, but we don't enforce it.
        user = re.sub(r'^acct:', '', user)

        if '@' not in user:
            return HttpResponse(
                    status = 404,
                    reason = 'absolute name required',
                    content = 'Please use the absolute form of the username.',
                    content_type = 'text/plain',
                    )

        username, hostname = user.split('@', 2)

        if hostname!=UN_CHAPEAU_SETTINGS['HOSTNAME']:
            return HttpResponse(
                    status = 404,
                    reason = 'not this server',
                    content = 'That user lives on another server.',
                    content_type = 'text/plain',
                    )

        try:
            queryset = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(
                    status = 404,
                    reason = 'no such user',
                    content = 'We don\'t have a user with that name.',
                    content_type = 'text/plain',
                    )

        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
