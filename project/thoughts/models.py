import re

from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        editable=False,
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('thoughts:category', kwargs={'category': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Thought(models.Model):
    author = models.CharField(
        blank=True,
        null=True,
        max_length=254
    )
    thought = models.TextField(
        max_length=2000
    )
    date = models.DateField(
        auto_now_add=True
    )
    enabled = models.BooleanField(
        default=True
    )
    first_letter = models.CharField(
        editable=False,
        max_length=1,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.author.split(" ")[0]}: {self.thought[:50]}'

    def save(self, *args, **kwargs):
        slug = slugify(self.thought)
        self.first_letter = re.sub('[0-9\-]', '', slug)[0]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("thoughts:detail", kwargs={"pk": self.pk})
