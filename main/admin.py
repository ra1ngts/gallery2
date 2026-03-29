from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from tabbed_admin import TabbedModelAdmin

from .models import (
    Gallery,
    Category,
    Profile,
    GalleryImage,
)


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(TranslationAdmin, TabbedModelAdmin):
    inlines = [GalleryImageInline]

    list_display = (
        'id',
        'title',
        'image',
        'category'
    )
    list_display_links = (
        'id',
        'title'
    )

    tab_main = (
        (None, {
            'fields': (
                'title_ru', 'title_en',
                'category_ru', 'category_en',
            )
        }),
    )

    tab_image = (
        GalleryImageInline,
    )

    tabs = [
        (_('Данные работы'), tab_main),
        (_('Изображения'), tab_image),
    ]

    group_fieldsets = True

    class Media:
        js = (
            'https://ajax.googleapis.com',
            'https://ajax.googleapis.com',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
        'updated_at'
    )
    list_display_links = (
        'id',
        'title'
    )
    list_filter = (
        'title',
    )
    ordering = ('order_by',)


@admin.register(Profile)
class ProfileAdmin(TranslationAdmin, TabbedModelAdmin):
    list_display = (
        'id',
        'name',
        'lastname',
        'phone',
        'email',
        'created_at',
        'updated_at'
    )
    list_display_links = (
        'id',
        'name'
    )

    tab_main = (
        (None, {
            'fields': (
                'name_ru', 'name_en',
                'lastname_ru', 'lastname_en',
                'image',
                'description_ru', 'description_en'
            )
        }),
    )

    tab_contacts = (
        (None, {
            'fields': (
                'phone',
                'email',
                'whatsapp',
                'telegram',
                'linkedin',
                'cv'
            )
        }),
    )

    tabs = [
        (_('Личные данные'), tab_main),
        (_('Контактные данные'), tab_contacts),
    ]

    group_fieldsets = True

    class Media:
        js = (
            'https://ajax.googleapis.com',
            'https://ajax.googleapis.com',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }