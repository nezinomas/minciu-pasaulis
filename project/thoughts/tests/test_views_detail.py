import pytest
from django.urls import resolve, reverse

from ...core.lib.test_utils import clean_content
from .. import views
from ..factories import ThoughtFactory

pytestmark = pytest.mark.django_db


def test_detail_func():
    view = resolve('/thought/9/')

    assert views.DetailView is view.func.view_class


def test_detail_404(client):
    url = reverse('thoughts:detail', kwargs={'pk': 666})
    response = client.get(url)

    assert response.status_code == 404


def test_detail_200(client):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client.get(url)

    assert response.status_code == 200


def test_detail_content(client):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client.get(url)
    content = clean_content(response.content)

    assert 'Author' in content
    assert 'Thought' in content


def test_detail_content_no_crud_buttons(client):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client.get(url)
    content = clean_content(response.content)

    assert 'hx-get=' not in content


def test_detail_content_row_id(client):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client.get(url)
    content = clean_content(response.content)

    assert f'id="row-id-{t.pk}"' in content


def test_detail_content_edit_button(client_logged):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)
    url_update = reverse('thoughts:update', kwargs={'pk': t.pk})

    assert f'hx-get="{url_update}"' in content


def test_detail_content_delete_button(client_logged):
    t = ThoughtFactory()
    url = reverse('thoughts:detail', kwargs={'pk': t.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)
    url_delete = reverse('thoughts:delete', kwargs={'pk': t.pk})

    assert f'hx-get="{url_delete}"' in content
