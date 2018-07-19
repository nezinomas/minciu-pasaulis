from django import template

register = template.Library()


@register.inclusion_tag('thoughts/includes/category_list.html')
def category_list(items, *args, **kwargs):
    return {
        'items': items,
        'border_position': kwargs.get('border_position')
    }
