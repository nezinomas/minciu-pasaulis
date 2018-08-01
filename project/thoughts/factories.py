from factory import DjangoModelFactory, SubFactory, Sequence

from . import models


class CategoriesFactory(DjangoModelFactory):
    class Meta:
        model = models.Categories

    title = Sequence(lambda n: 'Category{}'.format(n))


class ThoughtsFactory(DjangoModelFactory):
    class Meta:
        model = models.Thoughts

    author = 'Author'
    thought = 'Thought'
    category = SubFactory(CategoriesFactory)
