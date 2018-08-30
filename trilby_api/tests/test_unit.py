from django.test import TestCase, Client
from trilby_api.models import *

class UserTests(TestCase):

    fixtures = ['alicebobcarol']

    def test_status_count(self):

        carol = User.objects.get(username="carol")

        self.assertEqual(carol.statuses().count(), 0)

        for i in range(1, 13):
            Status.objects.create(
                    status='Hello world! {}'.format(i),
                    posted_by = carol,
                    )
            self.assertEqual(carol.statuses().count(), i)

    def test_following(self):

        bob = User.objects.get(username="bob")
        carol = User.objects.get(username="carol")

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

        bob.follow(carol)

        self.assertEqual(bob.is_following(carol), True)
        self.assertEqual(carol.is_following(bob), False)

        carol.follow(bob)

        self.assertEqual(bob.is_following(carol), True)
        self.assertEqual(carol.is_following(bob), True)

        bob.unfollow(carol)

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), True)

        carol.unfollow(bob)

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

    def test_locked_account_accepted(self):

        bob = User.objects.get(username="bob")
        carol = User.objects.get(username="carol")

        carol.locked = True
        carol.save()

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

        bob.follow(carol)

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

        self.assertEqual(carol.requesting_access.filter(pk=bob.pk).exists(), True)
        carol.dealWithRequest(bob, accept=True)
        self.assertEqual(carol.requesting_access.filter(pk=bob.pk).exists(), False)

        self.assertEqual(bob.is_following(carol), True)
        self.assertEqual(carol.is_following(bob), False)

    def test_locked_account_rejected(self):

        bob = User.objects.get(username="bob")
        carol = User.objects.get(username="carol")

        carol.locked = True
        carol.save()

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

        bob.follow(carol)

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

        self.assertEqual(carol.requesting_access.filter(pk=bob.pk).exists(), True)
        carol.dealWithRequest(bob, accept=False)
        self.assertEqual(carol.requesting_access.filter(pk=bob.pk).exists(), False)

        self.assertEqual(bob.is_following(carol), False)
        self.assertEqual(carol.is_following(bob), False)

class StatusTests(TestCase):

    fixtures = ['alicebobcarol']

    def test_sensitive_status(self):

        alice = User.objects.get(username="alice")

        for sensitive_by_default in (False, True):

            if sensitive_by_default:
                alice.default_sensitive = True
                alice.save()

            ordinary_status = Status.objects.create(
                posted_by = alice,
                status = 'I like cheese. It is delicious.',
                )

            self.assertEqual(ordinary_status.is_sensitive(),
                    sensitive_by_default)

            nsfw_status = Status.objects.create(
                posted_by = alice,
                status = 'I was rather naughty today.',
                sensitive = True,
                )

            self.assertEqual(nsfw_status.is_sensitive(), True)

            spoiler_status = Status.objects.create(
                posted_by = alice,
                spoiler_text = 'Spoilers for Jekyll and Hyde',
                status = 'They turn out to be the same guy.',
                )

            self.assertEqual(spoiler_status.is_sensitive(), True)

            nsfw_spoiler_status = Status.objects.create(
                posted_by = alice,
                sensitive = True,
                spoiler_text = 'Lex Luthor being naughty.',
                status = 'He stole 40 cakes.',
                )

            self.assertEqual(nsfw_spoiler_status.is_sensitive(), True)

class TimelineTests(TestCase):

    fixtures = ['alicebobcarol']

    pass
