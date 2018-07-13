from django.shortcuts import render
from django.views import View

class FrontPage(View):
    def get(self, request):
        result = render(
                request=request,
                template_name='frontpage.html',
                )

        return result
