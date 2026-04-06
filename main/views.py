from django.http import JsonResponse

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
    # category_slug = request.GET.get('category')

    # qs = Artwork.objects.select_related('category', 'technique', 'image').filter(
    #     is_published=True
    # )

    qs = Artwork.objects.select_related('category', 'technique').prefetch_related('images').filter(
        is_published=True
    )

    ctx = {
        'title': 'Gallery',
        'artworks': [ResultEncoder(artwork) for artwork in qs],
        # 'artworks': [ResultEncoder(artwork) for artwork in qs.filter(
        #     category__title=category_slug,
        # )]
    }

    return JsonResponse({
        'status': 'success',
        'ctx': ctx
    })