from django.contrib import admin

from .models import Element, ElementInElement


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_value', 'author', 'pub_date', )
    # list_editable = ('group', )
    search_fields = ('name', )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


# admin.site.register(Element)
admin.site.register(ElementInElement)
