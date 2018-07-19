from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
from oauth2_provider.models import Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import SuspiciousOperation
from un_chapeau.config import config
from .models import Status, User, Visibility
from .serializers import *
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json
import re

###########################

class Instance(View):

    def get(self, request, *args, **kwargs):

        result = {
            'uri': 'http://127.0.0.1',
            'title': config['INSTANCE_NAME'],
            'description': config['INSTANCE_DESCRIPTION'],
            'email': config['CONTACT_EMAIL'],
            'version': 'un_chapeau 0.0.1',
            'urls': {},
            'languages': config['LANGUAGES'],
            'contact_account': config['CONTACT_ACCOUNT'],
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

    def get(self, request):
        serializer = UserSerializerWithSource(request.user)
        return Response(serializer.data)

class Statuses(generics.ListCreateAPIView):

    queryset = Status.objects.all()
    serializer_class = StatusSerializer

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

    permission_classes = ()

    def get_queryset(self):
        return Status.objects.filter(visibility=Visibility('public').name)

########################################

class UserFeed(View):

    permission_classes = ()

    def get(self, request, username, *args, **kwargs):

        user = get_object_or_404(User, username=username)
        statuses = Status.objects.filter(posted_by=user)

        context = {
                'user': user,
                'statuses': statuses,
                'server_name': config['HOSTNAME'],
                'hubURL': config['HUB'],
            }

        result = render(
                request=request,
                template_name='account.atom.xml',
                context=context,
                content_type='application/atom+xml',
                )

        link_context = {
                'hostname': config['HOSTNAME'],
                'username': user.username,
                'acct': user.acct(),
                }

        links = ', '.join(
                [ '<{}>; rel="{}"; type="{}"'.format(
                    config.get(uri, username=user.username, acct=user.display_name),
                    rel, mimetype)
                    for uri, rel, mimetype in
                    [
                        ('USER_WEBFINGER_URLS',
                            'lrdd',
                            'application/xrd+xml',
                            ),

                        ('USER_FEED_URLS',
                            'alternate',
                            'application/atom+xml',
                            ),

                        ('USER_FEED_URLS',
                            'alternate',
                            'application/activity+json',
                            ),
                        ]
                    ])

        result['Link'] = links

        return result

########################################

class Webfinger(generics.GenericAPIView):
    """
    RFC7033 webfinger support.
    """

    serializer_class = WebfingerSerializer
    permission_classes = ()
    renderer_classes = (JSONRenderer, )

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

        if hostname!=config['HOSTNAME']:
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
        return Response(serializer.data,
                content_type='application/jrd+json; charset=utf-8')

########################################

class HostMeta(View):

    permission_classes = ()

    def get(self, request):

        context = {
                'server_name': config['HOSTNAME'],
            }

        result = render(
                request=request,
                template_name='host-meta.xml',
                context=context,
                content_type='application/jrd+xml',
                )

        return result


