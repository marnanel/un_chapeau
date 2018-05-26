"""un_chapeau URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
import oauth2_provider.views as oauth2_views
import trilby_api.urls
import trilby_api.views
import un_chapeau.settings as settings

##################################
# OAuth2 provider endpoints

oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

##################################################

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),

    path('oauth/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),

    path('api/', include((trilby_api.urls.endpoints, 'trilby_api'), namespace="trilby_api")),

    # XXX this should be in trilby_api's urls.py, not here
    path('users/<username>/feed', trilby_api.views.UserFeed.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

