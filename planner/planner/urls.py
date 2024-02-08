from django.contrib import admin
from django.urls import path
from diary.views import index, remove

urlpatterns = [
    path('', index, name="todo"),
    path('del/<str:item_id>', remove, name="del"),
    path('admin/', admin.site.urls),
]
