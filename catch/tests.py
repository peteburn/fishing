from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .models import Catch

User = get_user_model()

class CatchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        # create lookup entries the catches will reference
        from .models import Species, Venue, Method, Bait
        trout, _ = Species.objects.get_or_create(name='Trout')
        bass, _ = Species.objects.get_or_create(name='Bass')
        salmon, _ = Species.objects.get_or_create(name='Salmon')
        river, _ = Venue.objects.get_or_create(name='River')
        lake, _ = Venue.objects.get_or_create(name='Lake')
        sea, _ = Venue.objects.get_or_create(name='Sea')
        fly, _ = Method.objects.get_or_create(name='Fly fishing')
        spin, _ = Method.objects.get_or_create(name='Spinning')
        trolling, _ = Method.objects.get_or_create(name='Trolling')
        worm, _ = Bait.objects.get_or_create(name='Worm')
        insect, _ = Bait.objects.get_or_create(name='Insect')

        Catch.objects.create(user=self.user, date='2025-01-01', species=trout, venue=river, method=fly, bait=worm, length='short', weight=1.2)
        Catch.objects.create(user=self.other, date='2025-01-02', species=bass, venue=lake, method=spin, bait=insect, length='medium', weight=2.3)

    def test_list_requires_login(self):
        resp = self.client.get(reverse('catch_list'))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_user_sees_only_their_catches(self):
        self.client.login(username='test', password='pass')
        resp = self.client.get(reverse('catch_list'))
        # species are displayed by name
        self.assertContains(resp, 'Trout')
        # ensure the other user's catch doesn't appear in table cells
        self.assertNotContains(resp, '<td>Bass</td>')
        # filter by length
        resp2 = self.client.get(reverse('catch_list') + '?length=short')
        self.assertContains(resp2, '<td>Trout</td>')
        resp3 = self.client.get(reverse('catch_list') + '?length=medium')
        self.assertNotContains(resp3, '<td>Trout</td>')
        # show all users toggle
        resp_all = self.client.get(reverse('catch_list') + '?all=1')
        self.assertContains(resp_all, '<td>Bass</td>')
        self.assertContains(resp_all, '<td>other</td>')

    def test_logout_post(self):
        self.client.login(username='test', password='pass')
        # logout requires POST; a GET should not be allowed
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        resp_logout = self.client.post(reverse('logout'))
        self.assertIn(resp_logout.status_code, (302, 200))  # redirect or show page

    def test_create_catch_assigns_user(self):
        self.client.login(username='test', password='pass')
        # make sure the lookups exist so we can submit their IDs
        from .models import Species, Venue, Method, Bait
        salmon = Species.objects.get(name='Salmon')
        sea = Venue.objects.get(name='Sea')
        trolling = Method.objects.get(name='Trolling')
        from django.db import IntegrityError
        # submit using primary keys
        resp = self.client.post(reverse('catch_new'), {
            'date': '2025-02-01',
            'species': salmon.id,
            'venue': sea.id,
            'method': trolling.id,
            'bait': Bait.objects.get(name='Artificial lure').id,
            'length': 'long',
            'weight': '3.5',
        })
        self.assertEqual(Catch.objects.filter(user=self.user, species=salmon).count(), 1)
