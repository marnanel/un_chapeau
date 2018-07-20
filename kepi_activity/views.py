from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
import trilby_api.models as trilby
from un_chapeau.config import config

def render(data):
    result = JsonResponse(
            data=data,
            json_dumps_params={
                'sort_keys': True,
                'indent': 2,
                }
            )

    result['Content-Type'] = 'application/activity+json'

    return result

class User(View):
    def get(self, request, username):
        user = get_object_or_404(trilby.User, username=username)

        result = {
                "type": "Person", 
                "id": user.profileURL(),
                "name": user.display_name, 
                "preferredUsername": user.username,
                "url": user.profileURL(),
                "summary": user.note,

                "followers": user.followersURL(),
                "inbox": user.inboxURL(),
                "outbox": user.outboxURL(),
                "following": user.followingURL(),

                "endpoints": {
                    "sharedInbox": config['SHARED_INBOX_URL'],
                    }, 
                "icon": {
                    "url": user.avatar.url,
                    "type": "Image", 
                    "mediaType": "image/jpeg",
                    }, 
                "image": {
                    "url": user.header.url,
                    "type": "Image", 
                    "mediaType": "image/jpeg",
                    }, 
                "publicKey": {
                    "owner": user.profileURL(),
                    "id": '{}#main-key'.format(user.profileURL()),
                    "publicKeyPem": user.public_key,
                    }, 

                # XXX Mastodon has the "featured" collection here; what is it?
                "tag": [], 
                "attachment": [],
                "@context": [
                    "https://www.w3.org/ns/activitystreams", 
                    "https://w3id.org/security/v1", 
                    {
                        "schema": "http://schema.org#", 
                        "inReplyToAtomUri": "ostatus:inReplyToAtomUri", 
                        "movedTo": "as:movedTo", 
                        "conversation": "ostatus:conversation", 
                        "ostatus": "http://ostatus.org#", 
                        "atomUri": "ostatus:atomUri", 
                        "featured": "toot:featured", 
                        "value": "schema:value", 
                        "PropertyValue": "schema:PropertyValue", 
                        "sensitive": "as:sensitive", 
                        "toot": "http://joinmastodon.org/ns#", 
                        "Hashtag": "as:Hashtag", 
                        "manuallyApprovesFollowers": "as:manuallyApprovesFollowers", 
                        "focalPoint": {
                            "@id": "toot:focalPoint", 
                            "@container": "@list"
                            }, 
                        "Emoji": "toot:Emoji"
                        }
                    ], 
                "manuallyApprovesFollowers": False, 
        }

        return render(result)
