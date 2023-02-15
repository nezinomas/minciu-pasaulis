import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from . import models


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    password = make_password('123')


class CategoryFactory(DjangoModelFactory):

    class Meta:
        model = models.Category

    title = Sequence(lambda n: f'Category{n}')


class ThoughtFactory(DjangoModelFactory):
    class Meta:
        model = models.Thought

    author = 'Author'
    thought = 'Thought'
    category = SubFactory(CategoryFactory)
