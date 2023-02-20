import pytest
from django.urls import resolve, reverse

from ...core.lib.test_utils import clean_content
from .. import views
from ..factories import CategoryFactory, ThoughtFactory
from ..models import Thought

pytestmark = pytest.mark.django_db


def test_update_func():
    view = resolve('/thought/update/1/')

    assert views.UpdateView is view.func.view_class


def test_update_302(client):
    t = ThoughtFactory()
    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    response = client.get(url)

    assert response.status_code == 302


def test_update_200(client_logged):
    t = ThoughtFactory()
    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_update_load_form_post_link(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    form = clean_content(response.content)

    assert f'hx-post="{url}"' in form


def test_update_load_form(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    form = response.context['form'].as_p()

    assert 'Author' in form
    assert 'Thought' in form


def test_update_author(client_logged):
    t = ThoughtFactory()

    data = {
        'category': t.category.pk,
        'author': 'Updated Author',
        'thought': t.thought,
    }

    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    client_logged.post(url, data)

    actual = Thought.objects.get(pk=t.pk)

    assert actual.category == t.category
    assert actual.author == 'Updated Author'
    assert actual.thought == t.thought


def test_update_thought(client_logged):
    t = ThoughtFactory()

    data = {
        'category': t.category.pk,
        'author': t.author,
        'thought': 'Update Thought',
    }

    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    client_logged.post(url, data)

    actual = Thought.objects.get(pk=t.pk)

    assert actual.category == t.category
    assert actual.author == t.author
    assert actual.thought == 'Update Thought'


def test_update_category(client_logged):
    c = CategoryFactory()
    t = ThoughtFactory()

    data = {
        'category': c.pk,
        'author': t.author,
        'thought': t.thought,
    }

    url = reverse('thoughts:update', kwargs={'pk': t.pk})
    client_logged.post(url, data)

    actual = Thought.objects.get(pk=t.pk)

    assert actual.category == c
    assert actual.author == t.author
    assert actual.thought == t.thought
