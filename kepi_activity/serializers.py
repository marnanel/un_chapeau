from un_chapeau.config import config
from un_chapeau.constants import ATSIGN_CONTEXT
import trilby_api.models as trilby_models
from rest_framework_constant.fields import ConstantField
from rest_framework import serializers, mixins, pagination
from rest_framework.response import Response

class ActivityPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            # what if there's no next or prev?
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            'totalitems': self.page.paginator.count,
            'orderedItems': data,
            # partOf ...
            # @context...
            })

        # also, add Link header

class ActivitySerializer(serializers.ModelSerializer):

    def _to_representation(self, instance):

        result = super()._to_representation(instance)

        result.update({
            'context': ATSIGN_CONTEXT,
            'type': self.Meta.activity_type,
            })

        return result

class User(ActivitySerializer):

    class Meta:
        model = trilby_models.User

        activity_type = 'Person'

        fields = (
                'id', # profileserializers.URL()
                'name', # display_name
                'preferredUsername', # username
                'url', # profileserializers.URL()
                'summary', # note
                "manuallyApprovesFollowers", # ???

                'followers', # followersserializers.URL
                'following', # followingserializers.URL
                'inbox', # inboxserializers.URL
                'outbox', # outboxserializers.URL
                'endpoints',

                'icon',
                'image',
                'publicKey',

                'tag',
                'attachment',
                )

        # XXX MERGE FROM THIS
        #        "icon": {
        #            "url": user.avatar.url,
        #            "type": "Image", 
        #            "mediaType": "image/jpeg",
        #            }, 
        #        "image": {
        #            "url": user.header.url,
        #            "type": "Image", 
        #            "mediaType": "image/jpeg",
        #            }, 
        #        "publicKey": {
        #            "owner": user.profileserializers.URL(),
        #            "id": '{}#main-key'.format(user.profileserializers.URL()),
        #            "publicKeyPem": user.public_key,
        #            }, 

        # XXX Mastodon has the "featured" collection here; what is it?

        followers = serializers.URLField()
        following = serializers.URLField()
        inbox = serializers.URLField()
        outbox = serializers.URLField()

        icon = ConstantField(value='nyi')
        image = ConstantField(value='nyi')
        publicKey = ConstantField(value='nyi')

        tag = ConstantField(value=[])
        attachment = ConstantField(value=[])

        endpoints = ConstantField(value = {
            "sharedInbox": config['SHARED_INBOX_URL'],
            })

class ListFromUser(serializers.ModelSerializer):

    class Meta:
        model = trilby_models.User

        activity_type = 'OrderedCollection'

        fields = (
                'id',
                )

    id = serializers.CharField(
            source="profileURL",
            )


