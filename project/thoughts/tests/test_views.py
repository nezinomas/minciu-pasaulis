from django.test import TestCase
from django.urls import reverse, resolve

import time_machine
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
        view = resolve('/category/some/')
        self.assertEqual(view.func.view_class, views.ListView)

    def test_category_view_when_now_category(self):
        url = reverse('thoughts:category', kwargs={'category': 'xxx'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        # self.assertContains(resp, 'Tuščia')

    def test_category_view_category_with_no_thougths(self):
        factories.CategoriesFactory(title='C')

        url = reverse('thoughts:category', kwargs={'category': 'c'})
        print(url)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Tuščia')

    def test_category_view_ordering_then_category_has_no_childs_same_date(self):
        c = factories.CategoriesFactory(title='C')
        factories.ThoughtsFactory(thought='w', category=c)
        factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'c'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["object_list"][0]), 'Author: a')
        self.assertEqual(str(resp.context_data["object_list"][1]), 'Author: w')

    def test_category_view_ordering_then_category_has_no_childs_different_date(self):
        c = factories.CategoriesFactory(title='C')
        with time_machine.travel('2001-1-1'):
            factories.ThoughtsFactory(thought='w', category=c)

        with time_machine.travel('2000-1-1'):
            factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'c'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["object_list"][0]), 'Author: w')
        self.assertEqual(str(resp.context_data["object_list"][1]), 'Author: a')

    def test_category_view_ordering_then_category_with_childs_different_date(self):
        c = factories.CategoriesFactory(title='C', has_childs=True)
        with time_machine.travel('2001-1-1'):
            factories.ThoughtsFactory(thought='w', category=c)

        with time_machine.travel('2000-1-1'):
            factories.ThoughtsFactory(thought='a', category=c)

        url = reverse('thoughts:category', kwargs={'category': 'c'})
        resp = self.client.get(url)

        self.assertEqual(str(resp.context_data["object_list"][0]), 'Author: a')
        self.assertEqual(str(resp.context_data["object_list"][1]), 'Author: w')


class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        factories.ThoughtsFactory(thought='Lorem ipsum dolor sit amet, consectetur adipiscing elit.')

    def test_search_view(self):
        view = resolve('/results/')
        self.assertEqual(view.func.view_class, views.SearchView)

    def test_search_string_too_short(self):
        url = reverse('thoughts:search')
        response = self.client.get(url, {'q': '1'})
        self.assertContains(response, 'Tuščia')

    def test_search_string_empty(self):
        url = reverse('thoughts:search')
        response = self.client.get(url)
        self.assertContains(response, 'Tuščia')

    def test_search_empty(self):
        url = reverse('thoughts:search')
        response = self.client.get(url, {'q': 'xxx'})
        self.assertContains(response, 'Tuščia')

    def test_search_found_letters_lower(self):
        url = reverse('thoughts:search')
        response = self.client.get(url, {'q': 'lorem'})
        self.assertEqual(len(response.context[-2]['object_list']), 1)

    def test_search_found_author(self):
        url = reverse('thoughts:search')
        response = self.client.get(url, {'q': 'author'})
        self.assertEqual(len(response.context[-2]['object_list']), 1)

    def test_search_found_author_and_tought(self):
        url = reverse('thoughts:search')
        response = self.client.get(url, {'q': 'author lorem'})

        self.assertEqual(len(response.context[-2]['object_list']), 1)
