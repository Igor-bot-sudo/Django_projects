import re
import time
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from clock.models import AlarmClockModel


user_id = None


def clock(request):
    o = AlarmClockModel.objects.filter(user_id=user_id).all()
    alarms = [f'{i.hint} - {i.alarm_time}' if i.hint else f'{i.alarm_time}' for i in o]
    return render(request, "index.html", context={'alarms': alarms})


def get_time(request):
    let_play = False
    t = time.strftime('%H:%M')
    o = AlarmClockModel.objects.filter(user_id=user_id).filter(alarm_time=t)
    if o and time.strftime('%S') == '00':
        let_play = True
    return JsonResponse({"time": time.strftime('%H:%M:%S'), "let_play": let_play}, status=200)


def save(request):
    hour = request.POST['hour']
    minutes = request.POST['minutes']
    AlarmClockModel.objects.create(hint=request.POST['hint'], alarm_time=f'{hour}:{minutes}',
                                   user=User.objects.get(id=user_id))
    return redirect('clock')


def delete(request):
    alarm = request.POST['alarm']
    if ' - ' in alarm:
        alarm = alarm.split(' - ')[1]
    if re.fullmatch(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', alarm):
        AlarmClockModel.objects.filter(user_id=user_id).filter(alarm_time=alarm).delete()
    return redirect('clock')
