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

class Status(models.Model):

    # the spec calls this field "status", confusingly
    content = models.TextField()

    created_at = models.DateTimeField(default=now,
            editable=False)


    in_reply_to_id = models.ForeignKey('self',
            on_delete = models.CASCADE,
            )

    # XXX Media IDs here, when we've implemented Media

    sensitive = models.BooleanField(default=False)
    # applies to the media, not the text

    spoiler_text = models.CharField(max_length=255, default='')

    DIRECT = "direct"
    PRIVATE = "private"
    UNLISTED = "unlisted"
    PUBLIC = "public"

    VISIBILITY_CHOICES = (
            (DIRECT, DIRECT),
            (PRIVATE, PRIVATE),
            (UNLISTED, UNLISTED),
            (PUBLIC, PUBLIC),
            )

    visibility = models.CharField(max_length=255,
            choices = VISIBILITY_CHOICES,
            default = "public",
            )

    idempotency_key = models.CharField(max_length=255, default='')

    def is_sensitive(self):
        return self.spoiler_text!='' or self.sensitive

