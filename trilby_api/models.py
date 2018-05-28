from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
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

RELATIONSHIP_NONE = '-'
RELATIONSHIP_IS_FOLLOWING = 'F'
RELATIONSHIP_IS_BLOCKED_BY = 'B'
RELATIONSHIP_HAS_REQUESTED_ACCESS_TO = 'R'

RELATIONSHIP_CHOICES = (
        # ugh, that sounds like the title
        # of an eighties sex ed film

        (RELATIONSHIP_IS_FOLLOWING, 'is following'),
        (RELATIONSHIP_IS_BLOCKED_BY, 'is blocked by'),
        (RELATIONSHIP_HAS_REQUESTED_ACCESS_TO, 'has requested access to'),
        # RELATIONSHIP_NONE can't appear in a record
        )

#############################

def iso_date(date):
    return date.isoformat()+'Z'

#############################

class Media(object):

    # This will be a proper Model at some point,
    # but at present we only need it to be a class.

    def __init__(self, url,
            width=None, height=None):

        self.url = url
        self.width = width
        self.height = height

def default_avatar(variation=0):
    return Media(
            url='/static/un_chapeau/defaults/avatar_{0}.jpg'.format(
                variation % 10,
                ),
            width=120, height=120)

def default_header():
    return Media(
            url='/static/un_chapeau/defaults/default_header.jpg',
            width=700, height=335)

#############################

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

    # XXX horrible hack while I fix templates
    avatarOb = default_avatar()
    headerOb = default_header()

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

    ############### Relationship (friending, muting, blocking, etc)

    def _set_relationship(self, them, what, us=None):

        if us is None:
            us = self

        try:
            already = Relationship.objects.get(us=us, them=them)

            if what==RELATIONSHIP_NONE:
                already.delete()
            else:
                already.what = what
                already.save()

        except ObjectDoesNotExist:
            
            if what==RELATIONSHIP_NONE:
                # it ain't broken...
                return

            rel = Relationship(
                us = us,
                them = them,
                what = what)
            rel.save()

    def _get_relationship(self, them, us=None):

        if us is None:
            us = self

        try:
            rel = Relationship.objects.get(us=us, them=them)
            return rel.what

        except ObjectDoesNotExist:
            return RELATIONSHIP_NONE

    def block(self, someone):
        """
        Blocks another user. The other user should
        henceforth be unaware of our existence.

        See above for why we use "is blocked by"
        instead of "has blocked".
        """
        self._set_relationship(
                us=someone,
                them=self,
                what=RELATIONSHIP_IS_BLOCKED_BY)

        self._set_relationship(
                us=self,
                them=someone,
                what=RELATIONSHIP_NONE)

    def unblock(self, someone):
        """
        Unblocks another user.
        """

        if someone._get_relationship(self)!=RELATIONSHIP_IS_BLOCKED_BY:
            raise ValueError("%s wasn't blocked by %s" % (
                someone, self))

        self._set_relationship(
                us=someone,
                them=self,
                what=RELATIONSHIP_NONE)

    def follow(self, someone):
        """
        Follows another user.
        This has the side-effect of unblocking them;
        I don't know whether that's reasonable.

        If the other user's account is locked,
        this will request access rather than following.
        """

        if self._get_relationship(someone)==RELATIONSHIP_IS_BLOCKED_BY:
            raise ValueError("Can't follow: blocked.")

        if someone.locked:
            self._set_relationship(someone,
                    RELATIONSHIP_HAS_REQUESTED_ACCESS_TO)
        else:
            self._set_relationship(someone,
                    RELATIONSHIP_IS_FOLLOWING)

    def unfollow(self, someone):

        if self._get_relationship(someone)!=RELATIONSHIP_IS_FOLLOWING:
            raise ValueError("%s wasn't following %s" % (
                someone, self))

        self._set_relationship(someone,
                RELATIONSHIP_NONE)

    def is_following(self, someone):
        return self._get_relationship(someone)==RELATIONSHIP_IS_FOLLOWING

    def followRequests(self):
        """
        Returns the list of follow requests. This only makes
        sense for locked accounts.
        """
        return [r.us for r in Relationship.objects.filter(them=self,
                what=RELATIONSHIP_HAS_REQUESTED_ACCESS_TO)]

    def dealWithRequest(self, someone, accept=False):
        if someone._get_relationship(self)!=RELATIONSHIP_HAS_REQUESTED_ACCESS_TO:
            raise ValueError("%s hadn't requested access to %s" % (
                someone, self))

        if accept:
            new_relationship = RELATIONSHIP_IS_FOLLOWING
        else:
            new_relationship = RELATIONSHIP_NONE

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
            choices = VISIBILITY_CHOICES,
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
            choices = RELATIONSHIP_CHOICES,
            )

    def __str__(self):
        return '%s %s %s' % (
                self.us,
                dict(RELATIONSHIP_CHOICES)[self.what],
                self.them,
                )
