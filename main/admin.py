from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from tabbed_admin import TabbedModelAdmin

from .models import (
    Artwork,
    Category,
    Technique,
    Profile,
    ArtworkImage,
)


class ArtworkImageInline(admin.StackedInline):
    model = ArtworkImage
    extra = 1


@admin.register(Artwork)
class ArtworkAdmin(TranslationAdmin, TabbedModelAdmin):
    inlines = [ArtworkImageInline]

    list_display = (
        'id',
        'title',
        'year',
        'image',
        'category',
        'technique'
    )
    list_display_links = (
        'id',
        'title'
    )

    tab_main = (
        (None, {
            'fields': (
                'is_published',
                'order_by',
                'title_ru', 'title_en',
                'description_ru', 'description_en',
                'year',
                'category',
                'technique'
            )
        }),
    )

    tab_image = (
        ArtworkImageInline,
    )

    tabs = [
        (_('Информация о работе'), tab_main),
        (_('Изображения'), tab_image)
    ]

    group_fieldsets = True

    class Media:
        js = (
            'https://ajax.googleapis.com',
            'modeltranslation/js/tabbed_translation_fields.js'
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',)
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
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

    prepopulated_fields = {'slug': ('title_en',)}

    ordering = ('order_by',)


@admin.register(Technique)
class TechniqueAdmin(TranslationAdmin):
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

    prepopulated_fields = {'slug': ('title_en',)}

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
                'is_published',
                'order_by',
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
        (_('Контактные данные'), tab_contacts)
    ]

    group_fieldsets = True

    class Media:
        js = (
            'https://ajax.googleapis.com',
            'modeltranslation/js/tabbed_translation_fields.js'
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',)
        }