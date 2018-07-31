import random
from functools import reduce
from operator import or_

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Max
from django.db.models import Q

from .models import Categories, Thoughts

def get_random(model):
    max_id = model.objects.filter(enabled=True).aggregate(max_id=Max("id"))['max_id']
    if not max_id:
        return

    while True:
        pk = random.randint(1, max_id)
        obj = model.objects.filter(enabled=True, pk=pk).first()
        if obj:
            return obj


class HomeView(DetailView):
    template_name = 'thoughts/index.html'
    model = Thoughts

    def get_object(self, queryset=None):
        return get_random(Thoughts)


class CategoryView(ListView):
    template_name = 'thoughts/list.html'
    model = Thoughts
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(self):
        cid = get_object_or_404(Categories, slug=self.kwargs.get('category'))
        if cid.has_childs:
            ordering = ('first_letter', '-date')
        else:
            ordering = ('-date', 'first_letter')
        return Thoughts.objects.filter(category_id=cid.pk, enabled=True).order_by(*ordering)


class SearchView(ListView):
    template_name = 'thoughts/list.html'
    model = Thoughts
    context_object_name = 'items'

    def get_queryset(self):
        query = self.request.GET.get('q')
        results = None

        if query and len(query) >= 3:
            self.paginate_by = 50

            query_list = query.split()
            results = Thoughts.objects.filter(
                Q(enabled=True) & (
                    reduce(or_, (Q(author__icontains=q) for q in query_list)) | 
                    reduce(or_, (Q(thought__icontains=q) for q in query_list))
                )
            )
        return results
