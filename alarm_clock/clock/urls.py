from django.urls import path
from clock.views import clock, get_time, save, delete

urlpatterns = [
    path('save/', save, name='save'),
    path('delete/', delete, name='delete'),
    path('clock/', clock, name='clock'),
    path('gettime/', get_time, name='gettime')
]
