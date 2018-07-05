import django.db.models
import trilby_api.models
from django.utils.timezone import now

class Message(django.db.models.Model):

    data = django.db.models.CharField(
            max_length=255,
            )

    user = django.db.models.ForeignKey(
            trilby_api.models.User,
            on_delete = django.db.models.DO_NOTHING,
            )

    received_at = django.db.models.DateTimeField(
            default=now,
            editable=False,
            )

    def __str__(self):
        return '{} {}'.format(
                self.user,
                self.received_at,
                )
