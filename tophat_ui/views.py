from django.shortcuts import render, get_object_or_404
from django.views import View
from trilby_api.models import User, Status

class FrontPage(View):
    def get(self, request):
        result = render(
                request=request,
                template_name='frontpage.html',
                )

        return result

class UserPage(View):

    permission_classes = ()

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        statuses = Status.objects.filter(posted_by=user)

        context = {
                'user': user,
                'statuses': statuses,
                }

        result = render(
                request=request,
                context=context,
                template_name='userpage.html',
                )

        return result
