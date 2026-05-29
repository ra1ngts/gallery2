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
        # 'profile': {
        #     'technologies': _('Технологии'),
        #     'frontend': _('Фронтенд'),
        #     'backend': _('Бэкенд'),
        #     'tools': _('Инструменты'),
        #     'info': _('Список навыков пуст')
        # },
        # 'experience': {
        #     'info': _('Нет доступных записей')
        # },
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
        # 'utils': {
        #     'present': _('по настоящее время')
        # }
    }

    return TranslateDict