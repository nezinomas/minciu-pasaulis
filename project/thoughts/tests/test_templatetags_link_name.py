from django.test import TestCase
from ..templatetags.link_name import link_name


class LinkNameTests(TestCase):
    def test_page_number_01(self):
        expected = 'test?page=1'
        actual = link_name('test', 1)
        self.assertEqual(expected, actual)

    def test_page_number_02(self):
        expected = 'test?page=1'
        actual = link_name('test?page=1', 1)
        self.assertEqual(expected, actual)

    def test_page_number_03(self):
        expected = 'test?page=22'
        actual = link_name('test?page=1', 22)
        self.assertEqual(expected, actual)

    def test_page_number_04(self):
        expected = 'test?q=xx&page=1'
        actual = link_name('test?q=xx', 1)
        self.assertEqual(expected, actual)
