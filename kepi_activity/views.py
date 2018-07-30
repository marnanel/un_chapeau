# XXX several of these are probably superfluous
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
import trilby_api.models as trilby
import kepi_activity.serializers as serializers
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json
import re

def render(data):
    # XXX merge in
    result = JsonResponse(
            data=data,
            json_dumps_params={
                'sort_keys': True,
                'indent': 2,
                }
            )

    result['Content-Type'] = 'application/activity+json'

    return result

class UserView(generics.GenericAPIView):

    serializer_class = serializers.User
    permission_classes = ()

class FollowersView(generics.ListAPIView):

    serializer_class = serializers.ListFromUser
    permission_classes = ()

    def get_queryset(self):

        username=self.kwargs['username']

        return trilby.User.objects.filter(
                followers__username=username,
                ).order_by('date_joined')

class FollowingView(generics.ListAPIView):

    serializer_class = serializers.ListFromUser
    permission_classes = ()

    def get_queryset(self):

        username=self.kwargs['username']

        return trilby.User.objects.filter(
                following__username=username,
                ).order_by('date_joined')

