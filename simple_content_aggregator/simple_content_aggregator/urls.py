from django.contrib import admin
from django.urls import path
from content_aggregator.views import index, bs4_view, rss_view, show_page, pdf_export


urlpatterns = [
    path('bs4/', bs4_view, name='bs4'),
    path('rss/', rss_view, name='rss'),
    path('showpage/', show_page, name='showpage'),
    path('pdf/', pdf_export, name='pdf_export'),
    path('', index, name='home'),
    path('admin/', admin.site.urls),
]
