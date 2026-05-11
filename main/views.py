import os

from django.db.models import Window, F
from django.db.models.functions import RowNumber
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.files import get_thumbnailer

from gallery2 import settings
from .models import (
    Artwork,
    Category,
    Technique,
    Profile
)
from .utils import get_svelte_manifest


def get_thumb(image_field, size=(800, 0), crop=False):
    if not image_field:
        return None

    url_lower = image_field.url.lower()
    if url_lower.endswith('.svg') or '.svg?' in url_lower:
        return image_field.url

    try:
        options = {'size': size, 'crop': crop, 'quality': 80}
        return get_thumbnailer(image_field).get_thumbnail(options).url
    except Exception:
        return image_field.url


def ResultEncoder(obj):
    if isinstance(obj, Artwork):
        return {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'year': obj.year,
            'image': [
                get_thumb(img.image, size=(2000, 900)) for img in obj.images.all() if img.image
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
            'image': get_thumb(obj.image, size=(300, 300), crop=True) if obj.image else None,
            'description': obj.description,
            'phone': obj.phone,
            'email': obj.email,
            'whatsapp': obj.whatsapp,
            'telegram': obj.telegram,
            'linkedin': obj.linkedin,
            'cv': obj.cv
        }


def index(request):
    if request.headers.get('Accept') == 'application/json':
        try:
            annotated_works = Artwork.objects.filter(is_published=True).annotate(
                row=Window(
                    expression=RowNumber(),
                    partition_by=[F('category_id')],
                    order_by=F('id')
                )
            )

            artworks = Artwork.objects.select_related(
                'category',
                'technique'
            ).prefetch_related('images').filter(id__in=annotated_works.filter(row__lte=4).values('id'))

            return JsonResponse({
                'status': 'success',
                'title': _('Галерея'),
                'profile': ResultEncoder(Profile.get_profile_data()),
                'artworks': [ResultEncoder(artwork) for artwork in artworks],
                'featured_work': ResultEncoder(Artwork.objects.filter(is_featured=True).first()),
                'categories': list(Category.objects.values('slug', 'title'))
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    manifest = get_svelte_manifest(
        os.path.join(
            settings.BASE_DIR,
            'main',
            'static',
            'svelte',
            'assets',
            '.vite'
        )
    ).get('index.html', {})

    ctx = {
        'site_key': settings.RECAPTCHA_PUBLIC_KEY,
        'manifest_css': manifest.get('css', []),
        'manifest_js': manifest.get('file', ''),
        'title': Profile.get_profile_data().get_title
    }

    return render(request, 'main/index.html', ctx)


def category(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)

    except Http404:
        return JsonResponse({
            'status': 'error',
            'message': _('Категория не найдена')
        }, status=404)

    return JsonResponse({
        'status': 'success',
        'title': category.title,
        'artworks': [
            ResultEncoder(artwork) for artwork in Artwork.objects.select_related(
                'category',
                'image'
            ).prefetch_related('technique').filter(is_published=True, category=category)
        ],
    })
