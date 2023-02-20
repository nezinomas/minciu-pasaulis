import random
from django.db.models import Max


def get_random(model):
    max_id = model.objects.filter(enabled=True).aggregate(max_id=Max("id"))['max_id']
    if not max_id:
        return

    while True:
        pk = random.randint(1, max_id)
        if obj := model.objects.filter(enabled=True, pk=pk).first():
            return obj
