from django.utils.translation import gettext as _


def getTranslateDict():
    TranslateDict = {
        'app': {
            'sectionTitle': {
                'main': _('Главная'),
                'category': _('Категория'),
                'about': _('Обо мне'),
                'contact': _('Контакты')
            },
            'copyright': _('Все права защищены. Создано отцом с')
        },
        'main': {
            'view_all': _('Все работы'),
            'warning': _('Не найдено ни одной работы')
        },
        'category': {
            'all_years': _('Все годы'),
            'all_mediums': _('Все техники'),
            'year': _('Год'),
            'medium': _('Техника'),
            'warning': _('В категории не найдено ни одной работы'),
            'filters': _('Фильтры'),
            'show': _('Показать')
        },
        'contact': {
            'errors': {
                'name': _('Введите ваше имя'),
                'email': _('Введите корректный email'),
                'subject': _('Укажите тему'),
                'message': _('Введите текст сообщения')
            },
            'post': {
                'success': _('Сообщение успешно отправлено!'),
                'sending': _('Отправляем...'),
                'submit': _('Отправить')
            }
        },
    }

    return TranslateDict