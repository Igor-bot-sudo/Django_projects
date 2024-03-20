from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginUserForm, RegisterUserForm
from shortener import views



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'register/login.html'
    extra_context = {'title': 'Авторизация'}


class LogOutUser(LogoutView):
    success_url = reverse_lazy('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('login')


class LogOutUser(LogoutView):
    success_url = reverse_lazy('login')


def check_user(request):
    global views
    if request.method == "POST":
        user_name = request.POST['username']
        if User.objects.filter(username=user_name).exists():
            hash_ = User.objects.get(username=user_name).password
            if not check_password(password=request.POST['password'], encoded=hash_):
                messages.info(request, "Пароль введен не верно !!!")
                return redirect('login')
        else:
            messages.info(request, "Такого зарегистрированного пользователя нет !!!")
            return redirect('login')
        views.user_id = User.objects.get(username=user_name).id
        return redirect('make')
    else:
        return redirect('login')
