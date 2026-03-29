from modeltranslation.translator import register, TranslationOptions

from .models import Gallery, Category, Profile


@register(Gallery)
class GalleryTranslationOptions(TranslationOptions):
    fields = ('title', 'category')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'lastname', 'description')