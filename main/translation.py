from modeltranslation.translator import register, TranslationOptions

from .models import Artwork, Category, Technique, Profile


@register(Artwork)
class ArtworkTranslationOptions(TranslationOptions):
    fields = ('title', 'category', 'technique')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Technique)
class TechniqueTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('name', 'lastname', 'description')