from django.urls import path
from .views import *

endpoints = [

    path('v1/instance', Instance.as_view()),
    path('v1/apps', Apps.as_view()),
    path('v1/accounts/verify_credentials', Verify_Credentials.as_view()),
    path('v1/statuses', Statuses.as_view()),
    path('v1/timelines/public', PublicTimeline.as_view()),

    ]

