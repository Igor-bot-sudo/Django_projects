import random
import qrcode
from string import ascii_letters, digits
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django import forms
from django.utils import timezone
from shortener.models import ShortenerURLModel
from shortener.forms import ShortenerForm


user_id = None
punctuation = r"""!()*-<=>[\]^_`{|}~"""


class MakeShortURL(FormView):
    form_class = ShortenerForm
    template_name = 'shortener/index.html'
    extra_context = {'title': "Укорочение ссылки"}

    def get(self, request):
        form_ = ShortenerForm()
        page = {
            'form': form_,
        }
        return render(request, 'shortener/index.html', page)

    def post(self, request):
        class CustomizedForm(forms.ModelForm):
            class Meta:
                model = ShortenerURLModel
                fields = ('hint', 'long_link', 'short_link')

        host = request.get_host()
        long_link = request.POST['long_link']
        img_name = f"{str(timezone.now())[:-6].replace('.', '_').replace(':', '_').replace(' ', '_').replace('-', '_')}.jpg"
        filename = f'shortener/static/shortener/media/{img_name}'
        img = qrcode.make(long_link)
        img.save(filename)
        short_link = ''.join([random.choice(f'{ascii_letters}{digits}{punctuation}') for _ in range(8)])
        new_link = f'{host}/{short_link}'
        customized_post = request.POST.copy()
        customized_post['short_link'] = new_link
        customized_post['qr_code'] = img_name
        customized_post['user'] = user_id
        cf = CustomizedForm(customized_post)
        ShortenerURLModel.objects.create(hint=request.POST['hint'], long_link=long_link, short_link=short_link,
                                         qr_code=img_name, date=timezone.now(), user=User.objects.get(id=user_id))
        page = {
            'form': cf,
            'qr_code': img_name,
        }
        return render(request, 'shortener/index.html', page)


def short_url(request, url):
    try:
        o = ShortenerURLModel.objects.get(short_link=url)
        return redirect(o.long_link)
    except:
        return HttpResponse('<h1>Такой страницы не существует</h1>')
