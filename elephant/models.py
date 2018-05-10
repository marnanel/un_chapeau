from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from un_chapeau.settings import UN_CHAPEAU_SETTINGS

#############################

VISIBILITY_PRIVATE = 'X'
VISIBILITY_UNLISTED = 'U'
VISIBILITY_PUBLIC = 'P'
VISIBILITY_DIRECT = 'D'

VISIBILITY_CHOICES = (
        (VISIBILITY_PRIVATE, 'private'),
        (VISIBILITY_UNLISTED, 'unlisted'),
        (VISIBILITY_PUBLIC, 'public'),
        (VISIBILITY_DIRECT, 'direct'),
        )

#############################

RELATIONSHIP_IS_FOLLOWING = 'F'
RELATIONSHIP_HAS_BLOCKED = 'B'
RELATIONSHIP_HAS_MUTED = 'M'
RELATIONSHIP_HAS_MUTED_NOTIFICATIONS = 'N'
RELATIONSHIP_HAS_REQUESTED_ACCESS_TO = 'R'

RELATIONSHIP_CHOICES = (
        # ugh, that sounds like the title
        # of an eighties sex ed film

        (RELATIONSHIP_IS_FOLLOWING, 'is following'),
        (RELATIONSHIP_HAS_BLOCKED, 'has blocked'),
        (RELATIONSHIP_HAS_MUTED, 'has muted'),
        (RELATIONSHIP_HAS_MUTED_NOTIFICATIONS, 'has muted notifications'),
        (RELATIONSHIP_HAS_REQUESTED_ACCESS_TO, 'has requested access to'),
        )

#############################

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

    # XXX this should really use reverse()
    avatar = models.CharField(max_length=255,
            default='/static/un_chapeau/defaults/avatar_1.jpg')

    # XXX this should really use reverse()
    header = models.CharField(max_length=255,
            default='/static/un_chapeau/defaults/avatar_1.jpg')

    default_sensitive = models.BooleanField(
            default=False)

    default_visibility = models.CharField(
            max_length = 1,
            choices = VISIBILITY_CHOICES,
            default = VISIBILITY_PUBLIC,
            )

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
        return Status.objects.filter(posted_by=self).count()

    def avatar_static(self):
        # XXX
        return self.avatar

    def header_static(self):
        # XXX
        return self.header

    ############### Relationships (friending, muting, blocking, etc)

    def _make_relationship(self, someone, type_):
        rel = Relationship(
                us = self,
                them = someone,
                what = type_)
        rel.save()

    def _destroy_relationship(self, someone, type_):
        rel = Relationship.objects.get(
                us = self,
                them = someone,
                what = type_).delete()

    def _query_relationship(self, someone, type_):
        return Relationship.objects.filter(
                us = self,
                them = someone,
                what = type_).exists()

    def block(self, someone):
        self._make_relationship(someone,
                RELATIONSHIP_HAS_BLOCKED)

    def unblock(self, someone):
        self._destroy_relationship(someone,
                RELATIONSHIP_HAS_BLOCKED)

    def has_blocked(self, someone):
        return self._query_relationship(someone,
                RELATIONSHIP_HAS_BLOCKED)

    def _mute_type(self, with_notifications):
        if with_notifications:
            return RELATIONSHIP_HAS_MUTED_NOTIFICATIONS
        else:
            return RELATIONSHIP_HAS_MUTED

    def mute(self, someone,
            with_notifications=False):
        self._make_relationship(someone,
                self._mute_type(with_notifications))

    def unmute(self, someone,
            with_notifications=False):
        self._destroy_relationship(someone,
                self._mute_type(with_notifications))

    def has_muted(self, someone):
        return self._query_relationship(someone,
                self._mute_type(with_notifications))

    def follow(self, someone):
        self._make_relationship(someone,
                RELATIONSHIP_IS_FOLLOWING)

    def unfollow(self, someone):
        self._destroy_relationship(someone,
                RELATIONSHIP_IS_FOLLOWING)

    def is_following(self, someone):
        return self._query_relationship(someone,
                RELATIONSHIP_IS_FOLLOWING)

    def is_followed_by(self, someone):
        return Relationship.objects.filter(
                us = someone,
                them = self,
                what = RELATIONSHIP_IS_FOLLOWING).exists()

    def request_access(self, someone):
        self._make_relationship(someone,
                RELATIONSHIP_HAS_REQUESTED_ACCESS)

    def unrequest_access(self, someone):
        # I don't know whether that's the proper word
        self._destroy_relationship(someone,
                RELATIONSHIP_HAS_REQUESTED_ACCESS)

    def has_requested_access(self, someone):
        return self._query_relationship(someone,
                RELATIONSHIP_HAS_REQUESTED_ACCESS)

#############################

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

    sensitive = models.BooleanField(default=None)
    # applies to the media, not the text

    spoiler_text = models.CharField(max_length=255, default='')

    visibility = models.CharField(
            max_length = 1,
            choices = VISIBILITY_CHOICES,
            default = None,
            )

    idempotency_key = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):

        if self.visibility is None:
            self.visibility = self.posted_by.default_visibility
        if self.sensitive is None:
            self.sensitive = self.posted_by.default_sensitive

        super().save(*args, **kwargs)

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

class Relationship(models.Model):
    """
    A transitive relationship between two users.
    Don't use this class directly: use the accessors
    in User.
    """
    us = models.ForeignKey(User,
            on_delete = models.DO_NOTHING,
            related_name = 'active',
            )

    them = models.ForeignKey(User,
            on_delete = models.DO_NOTHING,
            related_name = 'passive',
            )

    what = models.CharField(
            max_length = 1,
            choices = RELATIONSHIP_CHOICES,
            )
