from django import forms
from .models import ShortenerURLModel


class ShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortenerURLModel
        fields = ('hint', 'long_link', 'short_link')
        labels = {'hint': 'Тема', 'long_link': 'Длинная ссылка', 'short_link': 'Короткая ссылка'}
