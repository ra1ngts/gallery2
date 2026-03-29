from modeltranslation.translator import register, TranslationOptions

from .models import Artwork, Category, Profile


@register(Artwork)
class ArtworkTranslationOptions(TranslationOptions):
    fields = ('title', 'category')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'lastname', 'description')