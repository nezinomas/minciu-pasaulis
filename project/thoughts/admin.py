from django.contrib import admin

from .models import Category, Thought


class CategoriesAdmin(admin.ModelAdmin):
    pass


class ThoughtsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoriesAdmin)
admin.site.register(Thought, ThoughtsAdmin)
