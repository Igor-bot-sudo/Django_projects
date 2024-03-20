from django.urls import path, re_path
from .views import MakeShortURL, short_url

urlpatterns = [
    re_path(r'^(?P<url>[0-9A-Za-z\!\(\)\*\-\<\=\>\[\\\]\^\_\`\{\|\}\~]{8})/$',
            short_url, name='short_url'),
    path('make/', MakeShortURL.as_view(), name='make'),
]
