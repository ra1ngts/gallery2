from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from tabbed_admin import TabbedModelAdmin

from .models import (
    Artwork,
    Category,
    Medium,
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
        'get_image',
        'category',
        'medium'
    )
    list_display_links = (
        'id',
        'title'
    )

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return mark_safe(f'<img src="{first_image.image.url}" width="60" style="border-radius: 5px;"/>')
        return '-'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images')

    get_image.short_description = _('Изображение')

    tab_main = (
        (None, {
            'fields': (
                'is_featured',
                'is_published',
                'order_by',
                'title_ru', 'title_en',
                'description_ru', 'description_en',
                'year',
                'category',
                'medium'
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


@admin.register(Medium)
class MediumAdmin(TranslationAdmin):
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