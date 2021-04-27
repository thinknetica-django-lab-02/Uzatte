from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from .models import Profile, Good, GoodProxy


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

    def make_archived(self, request, queryset):
        queryset.update(is_archive=True)

    make_archived.short_description = "Move to archive"
    actions = [make_archived]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_archive=False)


@admin.register(GoodProxy)
class GoodProxyAdmin(admin.ModelAdmin):
    """
    Admin class for Goods in Archive
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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_archive=True)

    def remove_from_arhive(self, request, queryset):
        queryset.update(is_archive=False)

    remove_from_arhive.short_description = "Remove from archive"
    actions = [remove_from_arhive]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Profile)
