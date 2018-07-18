from django.test import TestCase, Client
from .views import User

def UserTests(TestCase):

    def test_user_activity(self):

        activity = c.get('/users/alice/activity').json
        
        raise ValueError(str(activity))
