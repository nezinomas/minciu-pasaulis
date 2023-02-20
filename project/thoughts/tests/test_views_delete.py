import pytest
from django.urls import resolve, reverse

from ...core.lib.test_utils import clean_content
from .. import views
from ..factories import CategoryFactory, ThoughtFactory
from ..models import Thought

pytestmark = pytest.mark.django_db


def test_delete_func():
    view = resolve('/thought/delete/1/')

    assert views.DeleteView is view.func.view_class


def test_delete_302(client):
    t = ThoughtFactory()
    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    response = client.get(url)

    assert response.status_code == 302


def test_delete_200(client_logged):
    t = ThoughtFactory()
    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_delete_form_post_link(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    form = clean_content(response.content)

    assert f'hx-post="{url}"' in form


def test_delete_form_submit_button_data_pk(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    form = clean_content(response.content)

    assert f'data-pk="{t.pk}"' in form


def test_delete_form_text(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    form = clean_content(response.content)

    assert f'Ar tikrai nori ištrinti: <strong>{t}</strong>?' in form


def test_delete(client_logged):
    t = ThoughtFactory()

    url = reverse('thoughts:delete', kwargs={'pk': t.pk})
    client_logged.post(url, {})

    assert Thought.objects.all().count() == 0
