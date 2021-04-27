from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from .models import Profile, Good


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """
    Admin class for Good
    """
    list_filter = ('tags', 'publish_date')
    fieldsets = (
        ("General Info", {
            'fields': ('name', 'description', 'price', 'seller', 'in_stock')
        }),
        ('Tags & Categories', {
            'classes': ('collapse',),
            'fields': ('tags', 'category'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('image', 'publish_date'),
        })
    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Profile)

