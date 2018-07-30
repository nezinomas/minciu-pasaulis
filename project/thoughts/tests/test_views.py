from django.test import TestCase
from django.urls import reverse, resolve

from .. import views
from .. import factories

class HomeTests(TestCase):
    def test_home_view_when_empty_db(self):
        url = reverse('thoughts:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mintis pakeliui pasiklydo, bandykite paspausti F5.')

    def test_home_view_when_all_thougts_disabled(self):
        factories.ThoughtsFactory(enabled=False)

        url = reverse('thoughts:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mintis pakeliui pasiklydo, bandykite paspausti F5.')

    def test_home_view_when_all_thougts_deleted(self):
        th1 = factories.ThoughtsFactory()
        th2 = factories.ThoughtsFactory()
        th1.delete()
        th2.delete()

        url = reverse('thoughts:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mintis pakeliui pasiklydo, bandykite paspausti F5.')
