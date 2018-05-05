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

    locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=now,
            editable=False)

    note = models.CharField(max_length=255,
            default='')

    url = models.URLField(max_length=255,
            default='')

    moved_to = models.CharField(max_length=255,
            default='')

    def acct(self):
        # XXX for remote ones we need to spilt this up
        return self.username

    def followers_count(self):
        # XXX
        return 0

    def following_count(self):
        # XXX
        return 0

    def statuses_count(self):
        # XXX
        return 0

    def avatar(self):
        # XXX
        return '/static/un_chapeau/defaults/avatar_1.jpg'

    def avatar_static(self):
        # XXX
        return self.avatar()

    def header(self):
        # XXX
        return '/static/un_chapeau/defaults/header.jpg'

    def header_static(self):
        # XXX
        return self.header()

    def default_privacy(self):
        # XXX
        return 'public'

    def default_sensitive(self):
        # XXX
        return False

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

    VISIBILITY_VALUES = [DIRECT, PRIVATE, UNLISTED, PUBLIC]

    VISIBILITY_CHOICES = [(x,x) for x in VISIBILITY_VALUES]

    visibility = models.CharField(max_length=255,
            choices = VISIBILITY_CHOICES,
            default = "public",
            )

    idempotency_key = models.CharField(max_length=255, default='')

    def is_sensitive(self):
        return self.spoiler_text!='' or self.sensitive

    def __str__(self):
        return str(self.user) + " - " + self.content

    def _path_formatting(self, formatting):
        return UN_CHAPEAU_SETTINGS[formatting] % {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.posted_by.username,
                'id': self.id,
                }

    def url(self):
        return self._path_formatting('URL_FORMAT')

    def uri(self):
        return self._path_formatting('URI_FORMAT')

    def emojis(self):
        # I suppose we should do emojis eventually
        return []

    def reblog(self):
        # XXX
        return None

    def reblogs_count(self):
        # XXX
        return 0

    def favourites_count(self):
        # XXX
        return 0

    def reblogged(self):
        # XXX
        return False

    def favourited(self):
        # XXX
        return False

    def muted(self):
        # XXX
        return False

    def mentions(self):
        # XXX
        return []

    def media_attachments(self):
        # XXX
        return []

    def tags(self):
        # XXX
        return []

    def language(self):
        # XXX
        return 'en'

    def pinned(self):
        # XXX
        return False

    def in_reply_to_account_id(self):
        # XXX
        return None

    def application(self):
        # XXX
        return None

# XXX Need to wrap oauth2's Application. For now:
def application_as_json(app):
    return {
            "name": app.name,
            "website": app.website,
            }
