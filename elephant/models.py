from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):

    REQUIRED_FIELDS = ['username']
    # yes, the USERNAME_FIELD is the email, and not the username.
    # it's an oauth2 thing. just roll with it.
    USERNAME_FIELD = 'email'

    username = models.CharField(max_length=255,
            unique=True)

    email = models.EmailField(
            unique=True)

    display_name = models.CharField(max_length=255,
            default='')

    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=now,
            editable=False)

    note = models.CharField(max_length=255,
            default='')

    url = models.URLField(max_length=255,
            default='')

    moved_to = models.CharField(max_length=255,
            default='')
