from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.db.models import QuerySet, Model
from django.http import HttpRequest

from .models import Good, GoodProxy, Profile


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class ArrayFieldListFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a Good model `tags` ArrayField. """

    title = 'Tags'
    parameter_name = 'tags'

    def lookups(self, request: HttpRequest, model_admin: Model):

        tags = Good.objects.values_list("tags", flat=True)
        tags = [(tg, tg) for sublist in tags for tg in sublist if tg]
        tags = sorted(set(tags))
        return tags

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:

        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tags__contains=[lookup_value])
        return queryset


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """
    Admin class for Good
    """
    list_filter = (ArrayFieldListFilter, 'publish_date')
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
