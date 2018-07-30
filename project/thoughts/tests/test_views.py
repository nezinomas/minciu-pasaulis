from django.test import TestCase
from django.urls import reverse, resolve

from .. import views

class HomeTests(TestCase):
    def test_home_view_when_empty_db(self):
        url = reverse('thoughts:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mintis pakeliui pasiklydo, bandykite paspausti F5.')
