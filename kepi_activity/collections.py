from rest_framework import serializers
from un_chapeau.config import config

class CollectionView(object):

    def __init__(self, user):
        self._user = user
        self._collection = self._resultsset()

    def _resultsset(self):
        raise NotImplemented("abstract")

    def url(self):
        raise NotImplemented("abstract")
    
    def _page_url(self, page_number):
        return '{}?page={}'.format(
                self.url(),
                page_number,
                )

    def collection_dict(self):
        result= {
            "id": self.url(),
            "type":"OrderedCollection",
            "totalItems": len(self._collection),
        }

        if len(collection)!=0:
            result['first'] = self._page_url(1)

        return result

    def collection_page_dict(self, page_number):
        items_per_page = config['ITEMS_PER_PAGE']

        start = (page_number-1)*items_per_page

        items = self._collection[start:start+items_per_page]

        result = {
            "id": self._page_url(page_number),
            "type":"OrderedCollectionPage",
            "totalItems": len(self._collection),
            "partOf": self.url(),
            "orderedItems": items,
            }

        if start>0:
            result['prev'] = self._page_url(page_number-1)

        if (start+items_per_page)<len(self._collection):
            result['next'] = self._page_url(page_number+1)

        return result

#############################################

class Following(CollectionView):
    def _resultsset(self):
        return self._user.following()

class Followers(CollectionView):
    def _resultsset(self):
        return self._user.followers()


