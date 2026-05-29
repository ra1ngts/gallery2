from django import forms
from django.forms.widgets import EmailInput
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Имя'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Ваше имя')})
    )
    subject = forms.CharField(
        label=_('Тема'),
        max_length=200,
        required=True
    )
    message = forms.CharField(
        label=_('Сообщение'),
        widget=forms.Textarea(attrs={'placeholder': _('Ваше сообщение...'), 'rows': 5})
    )
    email = forms.EmailField(
        label=_('Электронная почта'),
        max_length=100,
        widget=EmailInput(attrs={'placeholder': _('example@example.com')})
    )