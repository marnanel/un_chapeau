from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
import oauth2_provider.views as oauth2_views
import trilby_api.urls
import trilby_api.views
import buckethat_salmon.views
import tophat_ui.views
import kepi_activity.views
import un_chapeau.settings as settings

##################################
# OAuth2 provider endpoints

oauth2_endpoint_views = [
    path('authorize', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

##################################################

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('accounts/login', auth_views.login, name='login'),
    path('accounts/logout', auth_views.logout, name='logout'),

    path('oauth/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),

    path('api/', include((trilby_api.urls.endpoints, 'trilby_api'), namespace="trilby_api")),

    path('users/<username>/feed', trilby_api.views.UserFeed.as_view()),
    path('.well-known/webfinger', trilby_api.views.Webfinger.as_view()),
    path('.well-known/host-meta', trilby_api.views.HostMeta.as_view()),

    path('users/<username>/salmon', buckethat_salmon.views.Salmon.as_view()),

    path('', tophat_ui.views.FrontPage.as_view()),
    path('about/', tophat_ui.views.FrontPage.as_view()),
    path('users/<username>', tophat_ui.views.UserPage.as_view()),

    path('users/<username>.json', kepi_activity.views.UserView.as_view()),
    path('users/<username>/following', kepi_activity.views.FollowingView.as_view()),
    path('users/<username>/followers', kepi_activity.views.FollowersView.as_view()),
    #path('users/<username>/outbox', kepi_activity.views.User.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

