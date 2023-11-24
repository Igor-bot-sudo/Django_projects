from django.urls import path
from kinopoisk.views import *


urlpatterns = [
    path('showpage/', show_page, name='show_page'),
    path('about_movie/', about_movie, name='about_movie'),
    path('search/', searchresultsview, name='search_results'),
    path('', index, name='home'),
]

handler404 = pageNotFound
