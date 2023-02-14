from .models import Category


def show_categories(context):
    return {
        'all_categories': Category.objects.all(),
    }
