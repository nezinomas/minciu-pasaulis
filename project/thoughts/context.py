from .models import Categories


def show_categories(context):
    return {
        'all_categories': Categories.objects.all(),
    }
