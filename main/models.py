import datetime

from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField


class Basic(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создано')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Обновлено')
    )

    class Meta:
        abstract = True


class BaseModelPublished(models.Model):
    is_published = models.BooleanField(
        verbose_name=_('Опубликовано'),
        default=True
    )

    class Meta:
        abstract = True


class BaseModelOrderby(models.Model):
    order_by = models.FloatField(
        help_text=_('Используйте дробные числа (например, 1.2), чтобы вставить запись между целыми числами без переименования остальных'),
        verbose_name=_('Порядок'),
        default=1.0
    )

    class Meta:
        abstract = True


class Artwork(Basic, BaseModelPublished, BaseModelOrderby):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Название')
    )
    description = models.TextField(
        help_text=_('Введите описание работы'),
        verbose_name=_('Описание работы')
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.datetime.now().year),
        ],
        help_text=_('Введите год создания работы'),
        verbose_name=_('Год создания работы')
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Загрузите изображение'),
        verbose_name=_('Изображение')
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='artworks_categories',
        verbose_name=_('Категория')
    )
    technique = models.ForeignKey(
        'Technique',
        on_delete=models.PROTECT,
        related_name='artwork_techniques',
        verbose_name=_('Техника исполнения')
    )
    is_featured = models.BooleanField(
        verbose_name=_('Особенная работа'),
        default=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Работа')
        verbose_name_plural = _('Работы')


class Category(Basic, BaseModelPublished, BaseModelOrderby):
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Название')
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Technique(Basic, BaseModelPublished, BaseModelOrderby):
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_('Название')
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Техника исполнения')
        verbose_name_plural = _('Техники исполнения')


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=_('Номер телефона должен быть в формате: "+79991234567". От 9 до 15 цифр.')
)


class Profile(Basic, BaseModelPublished, BaseModelOrderby):
    name = models.CharField(
        max_length=30,
        help_text=_('Введите имя'),
        verbose_name=_('Имя')
    )
    lastname = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text=_('Введите фамилию'),
        verbose_name=_('Фамилия')
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Загрузите изображение'),
        verbose_name=_('Изображение')
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_('Введите информацию о себе'),
        verbose_name=_('Описание')
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        validators=[phone_validator],
        help_text=_('Введите номер телефона'),
        verbose_name=_('Номер телефона')
    )
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
        max_length=40,
        help_text=_('Введите адрес вашей электронной почты'),
        verbose_name=_('Электронная почта')
    )
    whatsapp = models.URLField(
        null=True,
        blank=True,
        max_length=500,
        help_text=_('Введите ссылку на профиль WhatsApp'),
        verbose_name=_('WhatsApp')
    )
    telegram = models.URLField(
        null=True,
        blank=True,
        max_length=500,
        help_text=_('Введите ссылку на профиль Telegram'),
        verbose_name=_('Telegram')
    )
    linkedin = models.URLField(
        null=True,
        blank=True,
        max_length=500,
        help_text=_('Введите ссылку на профиль LinkedIn'),
        verbose_name=_('LinkedIn')
    )
    cv = models.URLField(
        null=True,
        blank=True,
        max_length=500,
        help_text = _('Введите ссылку на резюме'),
        verbose_name=_('Ссылка на резюме')
    )

    def __str__(self):
        return self.name

    @property
    def get_title(self):
        return f'{self.name} {self.lastname} - {_("портфолио")}'

    @classmethod
    def get_profile_data(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = _('Личная информация')
        verbose_name_plural = _('Личная информация')


class ArtworkImage(Basic, BaseModelPublished):
    artwork = models.ForeignKey(
        Artwork,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Изображение')
    )

    def __str__(self):
        return f'Изображение для {self.artwork.title} (ID: {self.id})'

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Художественная работа')
        verbose_name_plural = _('Художественные работы')