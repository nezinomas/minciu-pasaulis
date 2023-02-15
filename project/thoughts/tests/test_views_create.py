import pytest
from django.urls import resolve, reverse

from ...core.lib.test_utils import clean_content
from .. import views
from ..factories import CategoriesFactory, ThoughtsFactory
from ..models import Thought

pytestmark = pytest.mark.django_db


def test_create_func():
    view = resolve('/thought/create/')

    assert views.Create is view.func.view_class


def test_create_302(client):
    url = reverse('thoughts:create')
    response = client.get(url)

    assert response.status_code == 302


def test_create_200(client_logged):
    url = reverse('thoughts:create')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_create_load_form_post_link(client_logged):
    t = ThoughtsFactory()

    url = reverse('thoughts:create')
    response = client_logged.get(url)
    form = clean_content(response.content)

    assert f'hx-post="{url}"' in form


def test_create_load_form(client_logged):
    url = reverse('thoughts:create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="author"' in content
    assert '<textarea name="thought"' in content
    assert '<select name="category"' in content


def test_create_save_with_valid_data(client_logged):
    c = CategoriesFactory()

    data = {
        'author': 'Author',
        'thought': 'Thought',
        'category': c.pk
    }

    url = reverse('thoughts:create')
    client_logged.post(url, data)
    actual = Thought.objects.first()

    assert actual.category.title == c.title
    assert actual.author == 'Author'
    assert actual.thought == 'Thought'


def test_create_save_form_errors(client_logged):
    data = {}
    url = reverse('thoughts:create')
    response = client_logged.post(url, data)
    form = response.context['form']
    assert not form.is_valid()
    assert 'category' in form.errors
    assert 'thought' in form.errors
