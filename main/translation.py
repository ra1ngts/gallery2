from modeltranslation.translator import register, TranslationOptions

from .models import Artwork, Category, Medium, Profile


@register(Artwork)
class ArtworkTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Medium)
class MediumTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'lastname', 'description')