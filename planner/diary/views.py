from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .forms import TodoForm
from .models import Todo


user_id = None


def todo(request):
    class CustomizedForm(forms.ModelForm):
        class Meta:
            model = Todo
            fields = '__all__'

    first_name = User.objects.get(pk=user_id).first_name
    last_name = User.objects.get(pk=user_id).last_name
    item_list = Todo.objects.filter(user=user_id).order_by("-date")
    if request.method == "POST":
        customized_post = request.POST.copy()
        customized_post['user'] = User.objects.get(id=user_id)
        cf = CustomizedForm(customized_post)
        if cf.is_valid():
            cf.save()
            return redirect('todo')

    form = TodoForm()
    page = {
        "forms": form,
        "list": item_list,
        "title": "Список дел",
        "user_name": f'{first_name} {last_name}'
    }
    return render(request, 'todo/index.html', page)


def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "Запись удалена !!!")
    return redirect('todo')


def check_user(request):
    global user_id
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
        user_id = User.objects.get(username=user_name).id
        return redirect('todo')
    else:
        return redirect('login')
