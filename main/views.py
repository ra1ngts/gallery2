from django.http import JsonResponse

from .models import Artwork


def index(request):
    category_slug = request.GET.get('category')

    qs = Artwork.objects.select_related('category', 'technique', 'image').filter(
        is_published=True
    )

    ctx = {
        'title': 'Gallery',
        'artworks': qs.filter(
            category__title=category_slug,
        )
    }

    return JsonResponse({
        'status': 'success',
        'ctx': ctx
    })