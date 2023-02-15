from functools import reduce
from operator import or_

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 TemplateViewMixin, UpdateViewMixin)
from ..core.utils import random
from .forms import ThoughtForm
from .models import Category, Thought


class HomeView(DetailViewMixin):
    template_name = 'thoughts/index.html'

    def get_object(self, queryset=None):
        return random.get_random(Thought)


class ListView(ListViewMixin):
    model = Thought
    template_name = 'thoughts/list.html'
    paginate_by = 50

    def get_queryset(self):
        cid = get_object_or_404(Category, slug=self.kwargs.get('category'))
        if cid.has_childs:
            ordering = ('first_letter', '-date')
        else:
            ordering = ('-date', 'first_letter')
        return Thought.objects.filter(category_id=cid.pk, enabled=True).order_by(*ordering)


class SearchView(ListViewMixin):
    model = Thought
    template_name = 'thoughts/list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        results = None

        if query and len(query) >= 3:
            self.paginate_by = 50

            query_list = query.split()
            results = Thought.objects.filter(
                Q(enabled=True) & (
                    reduce(or_, (Q(author__icontains=q) for q in query_list)) |
                    reduce(or_, (Q(thought__icontains=q) for q in query_list))
                )
            )
        return results


class DetailView(DetailViewMixin):
    model = Thought


class CreateView(CreateViewMixin):
    model = Thought
    form_class = ThoughtForm
    template_name = 'thoughts/thought_form_create.html'


class UpdateView(UpdateViewMixin):
    model = Thought
    form_class = ThoughtForm
    template_name = 'thoughts/thought_form_update.html'

    def url(self):
        return reverse_lazy("thoughts:update", kwargs={"pk": self.kwargs["pk"]})


class DeleteView(DeleteViewMixin):
    model = Thought
    success_url = '/'
