from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest

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
            'fields': ('image', 'publish_date', 'is_publish'),
        })
    )

    def make_archived(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_archive=True)

    def publish_good(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_publish=True)

    def unpublish_good(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_publish=False)

    publish_good.short_description = "Publish"
    unpublish_good.short_description = "Unpublish"
    make_archived.short_description = "Move to archive"
    actions = [make_archived, publish_good, unpublish_good]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
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
            'fields': ('image', 'publish_date', 'is_publish'),
        })
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).filter(is_archive=True)

    def remove_from_archive(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_archive=False)

    remove_from_archive.short_description = "Remove from archive"

    actions = [remove_from_archive]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Profile)
