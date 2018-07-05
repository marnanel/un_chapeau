from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse
from trilby_api.models import User
from .models import Message

SUCCESS_REASON = 'Message received'
SUCCESS_CONTENT = 'Message received. Thank you.\n'

class Salmon(View):

    def post(self, request, username, *args, **kwargs):

        # XXX we should check the Content-Type as well,
        # though I need to find out what's permissible;
        # the reference implementation seems to want
        # application/atom+xml, which is strange, because
        # we're not sending Atom but a wrapper which
        # contains Atom.

        user = get_object_or_404(User,
                username=username)

        message = Message(
                user=user,
                data=request.body)

        message.save()

        return HttpResponse(
                status = 201,
                reason = SUCCESS_REASON,
                content = SUCCESS_CONTENT,
                content_type = 'text/plain',
                )
