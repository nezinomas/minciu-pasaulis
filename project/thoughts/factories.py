from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from . import models


class CategoriesFactory(DjangoModelFactory):

    class Meta:
        model = models.Categories

    title = Sequence(lambda n: f'Category{n}')


class ThoughtsFactory(DjangoModelFactory):
    class Meta:
        model = models.Thoughts

    author = 'Author'
    thought = 'Thought'
    category = SubFactory(CategoriesFactory)
