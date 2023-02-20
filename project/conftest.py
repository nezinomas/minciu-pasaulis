import pytest

from .thoughts.factories import UserFactory


@pytest.fixture()
def client_logged(client):
    UserFactory()
    client.login(username='bob', password='123')

    return client
