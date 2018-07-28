from rest_framework import serializers
from .models import User, Status, Visibility
from oauth2_provider.models import Application

#########################################

class _VisibilityField(serializers.CharField):
    # Is there really no general enum field?
    def to_representation(self, obj):
        return Visibility[obj].value

    def to_internal_value(self, obj):
        try:
            return Visibility(obj).name
        except KeyError:
            raise serializers.ValidationError('invalid visibility')

#########################################

class UserSerializer(serializers.ModelSerializer):

    avatar = serializers.CharField(
            read_only = True)
    header = serializers.CharField(
            read_only = True)

    # for the moment, treat these as the same.
    # the spec doesn't actually explain the difference!
    avatar_static = serializers.CharField(source='avatar',
            read_only = True)
    header_static = serializers.CharField(source='header',
            read_only = True)

    url = serializers.URLField(source='linked_url')

    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    statuses_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_statuses_count(self, obj):
        return obj.statuses().count()

    class Meta:
        model = User
        fields = (
                'id',
                'username',
                'acct',
                'display_name',
                'email',
                'locked',
                'avatar',
                'header',
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

#########################################

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


#########################################

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

    def create(self, validated_data):

        posted_by = self.context['request'].user
        validated_data['posted_by'] = posted_by

        result = Status.objects.create(**validated_data)
        return result

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

    visibility = _VisibilityField(
            required = False)

    def visibility_validation(self, value):
        if value not in Visibility:
            raise serializers.ValidationError('invalid visibility')

        return value

    idempotency_key = serializers.CharField(
            write_only = True,
            required = False)

#########################################

class WebfingerSerializer(serializers.ModelSerializer):

    # XXX need read_only=True

    class Meta:
        model = User
        fields = [
                'subject',
                'aliases',
                'links',
                ]

    def get_subject(self, instance):
        return 'acct:{}'.format(instance.acct())

    def get_aliases(self, instance):
        return [
                instance.profileURL(),
                ]

    def get_links(self, instance):
        return instance.links()

    subject = serializers.SerializerMethodField()
    aliases = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
