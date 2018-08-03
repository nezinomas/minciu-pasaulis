from django.test import TestCase
from django.urls import reverse, resolve

from freezegun import freeze_time

from .. import views
from .. import factories


class HomeTests(TestCase):
    def test_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, views.HomeView)

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

    def test_home_view_with_thought(self):
        factories.ThoughtsFactory()
        url = reverse('thoughts:home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Thought')
        self.assertContains(resp, 'Author')


class CategoryViewTest(TestCase):
    def test_category_view(self):
        view = resolve('/category/some')
        self.assertEqual(view.func.view_class, views.CategoryView)

    def test_category_view_when_now_category(self):
        url = reverse('thoughts:category', kwargs={'category': 'xxx'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        # self.assertContains(resp, 'Tuščia')

    def test_category_view_category_with_no_thougths(self):
        factories.CategoriesFactory(title='C')

        url = reverse('thoughts:category', kwargs={'category': 'C'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Tuščia')

    def test_category_view_ordering_then_category_has_no_childs_same_date(self):
        c = factories.CategoriesFactory(title='C')
        factories.ThoughtsFactory(thought='w', category=c)
        factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'C'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["items"][0]), 'Author: a')
        self.assertEqual(str(resp.context_data["items"][1]), 'Author: w')

    def test_category_view_ordering_then_category_has_no_childs_different_date(self):
        c = factories.CategoriesFactory(title='C')
        with freeze_time('2001-1-1'):
            factories.ThoughtsFactory(thought='w', category=c)

        with freeze_time('2000-1-1'):
            factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'C'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["items"][0]), 'Author: w')
        self.assertEqual(str(resp.context_data["items"][1]), 'Author: a')

    def test_category_view_ordering_then_category_with_childs_different_date(self):
        c = factories.CategoriesFactory(title='C', has_childs=True)
        with freeze_time('2001-1-1'):
            factories.ThoughtsFactory(thought='w', category=c)

        with freeze_time('2000-1-1'):
            factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'C'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["items"][0]), 'Author: a')
        self.assertEqual(str(resp.context_data["items"][1]), 'Author: w')
