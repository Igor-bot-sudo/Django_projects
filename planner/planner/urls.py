from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path
from diary.views import todo, remove, check_user
from registration.views import LoginUser, RegisterUser


urlpatterns = [
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html'
         ), name='password_reset'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html"
         ),
         name='password_reset_confirm'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),
    path('check_user/', check_user, name='check_user'),
    path('logout/', LoginUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('todo/', todo, name='todo'),
    path('del/<str:item_id>', remove, name='del'),
    path('admin/', admin.site.urls),
    path('', LoginUser.as_view(), name='login'),
]
