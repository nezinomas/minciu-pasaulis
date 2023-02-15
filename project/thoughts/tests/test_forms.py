
import pytest

from ..forms import ThoughtForm
from ..factories import CategoryFactory
pytestmark = pytest.mark.django_db


def test_thought_init():
    ThoughtForm()


def test_thought_init_fields():
    form = ThoughtForm().as_p()

    assert '<input type="text" name="author"' in form
    assert '<textarea name="thought"' in form
    assert '<select name="category"' in form


def test_thought_valid_data():
    c = CategoryFactory()

    form = ThoughtForm(data={
        'author': 'Author',
        'thought': 'Thought',
        'category': c.pk
    })

    assert form.is_valid()

    data = form.save()

    assert data.author == 'Author'
    assert data.thought == 'Thought'
    assert data.category.title == c.title


def test_thought_blank_data():
    form = ThoughtForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2
    assert 'category' in form.errors
    assert 'thought' in form.errors
