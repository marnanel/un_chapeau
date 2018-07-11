from enum import Enum
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.files.images import ImageFile
from un_chapeau.settings import UN_CHAPEAU_SETTINGS
from trilby_api.crypto import Key

#############################

class Visibility(Enum):
    P = 'public'
    X = 'private'
    U = 'unlisted'
    D = 'direct'

#############################

class RelationshipType(Enum):
    F = 'is following'
    B = 'is blocked by'
    R = 'has requested access to'

#############################

def iso_date(date):
    return date.isoformat()+'Z'

#############################

def default_avatar():
    path = 'defaults/avatar_{0}.jpg'.format(randint(0,9))

    return ImageFile(
            open(
                StaticFilesStorage().path(path), 'rb')
            )

def default_header():
    path = 'defaults/header.jpg'
    return ImageFile(
            open(
                StaticFilesStorage().path(path), 'rb')
            )

#############################

def avatar_upload_to(instance, filename):
    return 'avatars/%s.jpg' % (
            instance.username,
            )

def header_upload_to(instance, filename):
    return 'headers/%s.jpg' % (
            instance.username,
            )

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

    note = models.CharField(max_length=255,
            default='')

    linked_url = models.URLField(max_length=255,
            default='')

    moved_to = models.CharField(max_length=255,
            default='')

    avatar = models.ImageField(
            upload_to = avatar_upload_to,
            default=None,
            )

    header = models.ImageField(
            upload_to = header_upload_to,
            default=None,
            )

    private_key = models.BinaryField(
            editable = False,
            )
    magic_envelope_public_key = models.CharField(
            max_length=255,
            editable = False,
            )

    def save(self, *args, **kwargs):
        if not self.private_key:
            key = Key()
            self.private_key = key.as_pem()
            self.magic_envelope_public_key = key.magic_envelope()

        if not self.avatar:
            self.avatar = default_avatar()

        if not self.header:
            self.header = default_header()

        super().save(*args, **kwargs)

    default_sensitive = models.BooleanField(
            default=False)

    default_visibility = models.CharField(
            max_length = 1,
            choices = [(tag.name, tag.value) for tag in Visibility],
            default = Visibility('public').name,
            )

    def created_at(self):
        # Alias for Django's date_joined. Mastodon calls this created_at,
        # and it makes things easier if the model can call it that too.
        return self.date_joined

    def acct(self):
        # XXX obviously we need to do something else for remote accounts
        return '{0}@{1}'.format(
                self.username,
                UN_CHAPEAU_SETTINGS['HOSTNAME'],
                )

    def followers_count(self):
        return Relationship.objects.filter(them=self).count()

    def following_count(self):
        return Relationship.objects.filter(us=self).count()

    def statuses_count(self):
        return Status.objects.filter(posted_by=self).count()

    def avatar_static(self):
        # XXX
        return self.avatar

    def header_static(self):
        # XXX
        return self.header

    def updated(self):
        return Status.objects.filter(posted_by=self).latest('created_at').created_at

    ############### Relationship (friending, muting, blocking, etc)

    def _set_relationship(self, them, what, us=None):

        if us is None:
            us = self

        try:
            already = Relationship.objects.get(us=us, them=them)

            if what is None:
                already.delete()
            else:
                already.what = what.name
                already.save()

        except ObjectDoesNotExist:
            
            if what is None:
                # it ain't broken...
                return

            rel = Relationship(
                us = us,
                them = them,
                what = what.name)
            rel.save()

    def _get_relationship(self, them, us=None):

        if us is None:
            us = self

        try:
            rel = Relationship.objects.get(us=us, them=them)
            return RelationshipType[rel.what]

        except ObjectDoesNotExist:
            return None

    def block(self, someone):
        """
        Blocks another user. The other user should
        henceforth be unaware of our existence.
        """
        self._set_relationship(
                us=someone,
                them=self,
                what=RelationshipType('is blocked by'))

        self._set_relationship(
                us=self,
                them=someone,
                what=None)

    def unblock(self, someone):
        """
        Unblocks another user.
        """

        if someone._get_relationship(self)!=RelationshipType('is blocked by'):
            raise ValueError("%s wasn't blocked by %s" % (
                someone, self))

        self._set_relationship(
                us=someone,
                them=self,
                what=None)

    def follow(self, someone):
        """
        Follows another user.
        This has the side-effect of unblocking them;
        I don't know whether that's reasonable.

        If the other user's account is locked,
        this will request access rather than following.
        """

        if self._get_relationship(someone)==RelationshipType('is blocked by'):
            raise ValueError("Can't follow: blocked.")

        if someone.locked:
            self._set_relationship(someone,
                    RelationshipType('has requested access to'))
        else:
            self._set_relationship(someone,
                    RelationshipType('is following'))

    def unfollow(self, someone):

        if self._get_relationship(someone)!=RelationshipType('is following'):
            raise ValueError("%s wasn't following %s" % (
                someone, self))

        self._set_relationship(someone,
                None)

    def is_following(self, someone):
        return self._get_relationship(someone)==RelationshipType('is following')

    def followRequests(self):
        """
        Returns the list of follow requests. This only makes
        sense for locked accounts.
        """
        return [r.us for r in Relationship.objects.filter(them=self,
                what=RelationshipType('has requested access to').name)]

    def dealWithRequest(self, someone, accept=False):
        if someone._get_relationship(self)!=RelationshipType('has requested access to'):
            raise ValueError("%s hadn't requested access to %s" % (
                someone, self))

        if accept:
            new_relationship = RelationshipType('is following')
        else:
            new_relationship = None

        self._set_relationship(
                us=someone, them=self,
                what=new_relationship)

    def profileURL(self):
        return UN_CHAPEAU_SETTINGS['USER_URLS'] % {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.username,
                }

    def feedURL(self):
        return UN_CHAPEAU_SETTINGS['USER_FEED_URLS'] % {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.username,
                }

    def salmonURL(self):
        return UN_CHAPEAU_SETTINGS['USER_SALMON_URLS'] % {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.username,
                }

    def public_key(self):
        return 'data:{},{}'.format(
                'application/magic-public-key',
                self.magic_envelope_public_key,
                )

    def links(self):
        return [
                {
                'rel': 'http://webfinger.net/rel/profile-page',
                'type': 'text/html',
                'href': self.profileURL(),
                },
                {
                'rel': 'http://schemas.google.com/g/2010#updates-from',
                'type': 'application/atom+xml',
                'href': self.feedURL(),
                },
                {
                'rel': 'self',
                'type': 'application/activity+json',
                'href': self.feedURL(),
                },
                {
                'rel': 'salmon',
                'href': self.salmonURL(),
                },
                {
                'rel': 'magic-public-key',
                'href': self.public_key(),
                },
                {
                'rel': 'http://ostatus.org/schema/1.0/subscribe',
                'template': UN_CHAPEAU_SETTINGS['AUTHORIZE_FOLLOW_TEMPLATE'] % {
                    'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                    },
                },
               ]

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

    spoiler_text = models.CharField(max_length=255, default='',
            blank=True)

    visibility = models.CharField(
            max_length = 1,
            choices = [(tag.name, tag.value) for tag in Visibility],
            default = None,
            )

    idempotency_key = models.CharField(max_length=255, default='',
            blank=True)

    def save(self, *args, **kwargs):
        if self.visibility is None:
            self.visibility = self.posted_by.default_visibility
        if self.sensitive is None:
            self.sensitive = self.posted_by.default_sensitive

        super().save(*args, **kwargs)

    def is_sensitive(self):
        return self.spoiler_text!='' or self.sensitive

    def title(self):
        """
        Returns the title of this status.

        This isn't anything useful, but the Atom feed
        requires it. So we return some vacuous string.
        """ 
        return 'Status by %s' % (self.posted_by.username, )

    def __str__(self):
        return str(self.posted_by) + " - " + self.content

    def _path_formatting(self, formatting):
        return UN_CHAPEAU_SETTINGS[formatting] % {
                'hostname': UN_CHAPEAU_SETTINGS['HOSTNAME'],
                'username': self.posted_by.username,
                'id': self.id,
                }

    def url(self):
        """
        Returns the URL of the user's page on *this* server.
        """
        return self._path_formatting('STATUS_URLS')

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
        if self.in_reply_to_id is None:
            return None
        else:
            return self.in_reply_to_id.posted_by.pk

    def application(self):
        # XXX
        return None

    def atomURL(self):
        return self._path_formatting('STATUS_FEED_URLS')

class Relationship(models.Model):
    """
    A transitive relationship between two users.
    Don't use this class directly: use the accessors
    in User.
    """

    class Meta:
        unique_together = (('us', 'them'),)

        indexes = [
            models.Index(fields=['us', 'them']),
        ]

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
            choices = [(tag.name, tag.value)
                for tag in RelationshipType
                if tag.value!='none'],
            )

    def __str__(self):
        return '%s %s %s' % (
                self.us,
                RelationshipType[self.what],
                self.them,
                )
