from django.test import TestCase, Client
from .views import User

class UserTests(TestCase):

    def test_user_activity(self):

        c = Client()
        activity = c.get('/users/alice/activity').json()
        
        raise ValueError(str(activity))
