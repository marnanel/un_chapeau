from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from un_chapeau.settings import UN_CHAPEAU_SETTINGS

def iso_date(date):
    return date.isoformat()+'Z'

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


    def as_json(self,
            include_source=False):

        result = {
            'id': self.id,
            'username': self.username,
            'acct': self.username, # XXX for remote ones we need to split this up
            'display_name': self.display_name,
            'locked': self.is_locked,
            'created_at': iso_date(self.created_at),
            'note': self.note,
            'url': self.url,
            'avatar': '/static/un_chapeau/defaults/avatar_1.jpg',
            'avatar_static': '/static/un_chapeau/defaults/avatar_1.jpg',
            'header': '/static/un_chapeau/defaults/header.jpg',
            'header_static': '/static/un_chapeau/defaults/header.jpg',
            'followers_count': 0,
            'following_count': 0,
            'statuses_count': 0,
        }

        if include_source:
            result['source'] = {
                'privacy': 'public',
                'sensitive': False,
                'note': self.note,
                }

        return result

class Status(models.Model):

    class Meta:
        verbose_name_plural = "statuses"

    posted_by = models.ForeignKey(User,
            on_delete = models.CASCADE,
            default = 1, # to pacify makemigrations
            )

    # the spec calls this field "status", confusingly
    content = models.TextField()

    created_at = models.DateTimeField(default=now,
            editable=False)

    in_reply_to_id = models.ForeignKey('self',
            on_delete = models.CASCADE,
            blank = True,
            null = True,
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

    def __str__(self):
        return str(self.user) + " - " + self.content

    def as_json(self):

        path_formatting = {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.posted_by.username,
                'id': self.id,
                }

        result = {
                "id": self.posted_by.as_json(),
                "url": UN_CHAPEAU_SETTINGS['URL_FORMAT'] % path_formatting,
                "uri": UN_CHAPEAU_SETTINGS['URI_FORMAT'] % path_formatting,
                "account": self.posted_by.as_json(),
                "content": self.content,
                'created_at': iso_date(self.created_at),
                "emojis": [],
                "reblogs_count": 0,
                "favourites_count": 0,
                "reblogged": False,
                "favourited": False,
                "muted": False,
                "sensitive": self.is_sensitive(),
                "spoiler_text": self.spoiler_text,
                "visibility": self.visibility,
                "media_attachments": [],
                "mentions": [],
                "tags": [],
                "language": 'en', # XXX
                "pinned": False,
                "in_reply_to_id": None, # XXX
                "in_reply_to_account_id": None, # XXX
                "application": None, # XXX
            }
        return result

# XXX Need to wrap oauth2's Application. For now:
def application_as_json(app):
    return {
            "name": app.name,
            "website": app.website,
            }
