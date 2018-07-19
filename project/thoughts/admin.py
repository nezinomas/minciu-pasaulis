from django.contrib import admin

from .models import Categories, Thoughts


class CategoriesAdmin(admin.ModelAdmin):
    pass


class ThoughtsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Thoughts, ThoughtsAdmin)
