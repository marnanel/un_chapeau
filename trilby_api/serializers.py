from rest_framework import serializers
from .models import User, Status
from oauth2_provider.models import Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                'id',
                'username',
                'acct',
                'display_name',
                'email',
                'locked',
                'created_at',
                'followers_count',
                'following_count',
                'statuses_count',
                'note',
                'url',
                'avatar',
                'avatar_static',
                'header',
                'header_static',
                'moved_to',
                )

class UserSerializerWithSource(UserSerializer):

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + (
            'source',
            )

    source = serializers.SerializerMethodField()

    def get_source(self, instance):
        return {
                'privacy': instance.default_visibility,
                'sensitive': instance.default_sensitive,
                'note': instance.note,
                }


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'url', 'uri',
                'account',
                'in_reply_to_id',
                'in_reply_to_account_id',
                'reblog',
                'status',
                'content',
                'created_at',
                'emojis',
                'reblogs_count',
                'favourites_count',
                'reblogged',
                'favourited',
                'muted',
                'sensitive',
                'spoiler_text',
                'visibility',
                'media_attachments',
                'mentions',
                'tags',
                'application',
                'language',
                'pinned',
                'idempotency_key',
                )

    id = serializers.IntegerField(
            read_only = True)

    account = UserSerializer(
            source = 'posted_by',
            read_only = True)

    status = serializers.CharField(
            write_only = True,
            source = 'content')

    content = serializers.CharField(
            read_only = True)

    created_at = serializers.DateTimeField(
            read_only = True)

    in_reply_to_id = serializers.PrimaryKeyRelatedField(
            queryset=Status.objects.all,
            required = False)

    url = serializers.URLField(
            read_only = True)

    uri = serializers.URLField(
            read_only = True)

    # TODO Media

    sensitive = serializers.BooleanField(
            required = False)
    spoiler_text = serializers.CharField(
            required = False)

    visibility = serializers.CharField(
            required = False)

    def visibility_validation(self, value):
        if value not in Status.VISIBILITY_VALUES:
            raise serializers.ValidationError(
                    'valid visibilities are: '+(' '.join(Status.VISIBILITY_VALUES)))
        return value

    idempotency_key = serializers.CharField(
            write_only = True,
            required = False)
