from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import (
    Artwork,
    Category,
    Technique,
    Profile
)


def ResultEncoder(obj):
    if isinstance(obj, Artwork):
        return {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'year': obj.year,
            'image': [
                img.image.url for img in obj.images.all() if img.image
            ],
            'category': ResultEncoder(obj.category) if obj.category else None,
            'technique': ResultEncoder(obj.technique) if obj.technique else None
        }

    if isinstance(obj, Category):
        return {
            'id': obj.id,
            'title': obj.title,
            'slug': obj.slug
        }

    if isinstance(obj, Technique):
        return {
            'id': obj.id,
            'title': obj.title,
            'slug': obj.slug
        }

    if isinstance(obj, Profile):
        return {
            'id': obj.id,
            'name': obj.name,
            'lastname': obj.lastname,
            'image': obj.image.url if obj.image else None,
            'description': obj.description,
            'phone': obj.phone,
            'email': obj.email,
            'whatsapp': obj.whatsapp,
            'telegram': obj.telegram,
            'linkedin': obj.linkedin,
            'cv': obj.cv
        }


def index(request):
    ctx = {
        'title': _('Галерея'),
        'artworks': [
            ResultEncoder(artwork) for artwork in Artwork.objects.select_related(
                'category',
                'technique'
            ).prefetch_related('images').filter(is_published=True)
        ]
    }

    return JsonResponse({
        'status': 'success',
        'ctx': ctx
    })


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    ctx = {
        'title': category.title,
        'artworks': [
            ResultEncoder(artwork) for artwork in Artwork.objects.select_related(
                'category',
                'image'
            ).prefetch_related('technique').filter(is_published=True, category=category)
        ]
    }

    return JsonResponse({
        'status': 'success',
        'ctx': ctx
    })