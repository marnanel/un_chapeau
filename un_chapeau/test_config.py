from django.test import TestCase
from un_chapeau.config import config
from .settings import UN_CHAPEAU

class ConfigTest(TestCase):

    def test_gets(self):

        UN_CHAPEAU['HOSTNAME'] = 'wombat.example.com'
        UN_CHAPEAU['URL'] = 'https://{hostname}/spong'

        self.assertEqual(
                config['HOSTNAME'],
                'wombat.example.com',
                )
        self.assertEqual(
                config.get('HOSTNAME'),
                'wombat.example.com',
                )
        self.assertEqual(
                config.get('URL'),
                'https://wombat.example.com/spong',
                )
