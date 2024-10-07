import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import csrf_token
import json
from . import models


def home_view(req,**opt):
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    available_camp = list(models.Camp.objects.filter(end__gt=curr_date).values())
    
    for i in range(len(available_camp)):
        available_camp[i]['owned_id'] = models.Admin.objects.filter(id=available_camp[i]['owned_id']).values()[0]['belongs']
    
    context = {'camps':available_camp}
    context.update(opt)
    
    return render(req,'home/index.html',context=context)

def login_view(req):
    return render(req,'home/login.html')

def donor_login(req):
    user, passwrd = req.POST.get('user',None), req.POST.get('passwrd',None)
    
    if not user or not passwrd: return redirect(reverse('home'))
    
    userThis = models.Donor.objects.filter(id=user).values()
    
    if userThis:
        return redirect(reverse('home',kwargs={"error":'Authetication error'}))
    
    userThis = userThis[0]
    
    if check_password(passwrd,userThis['passwrd']):
        req.session['user'] = userThis['name']
        return redirect(reverse('home',kwargs={"error":'Authetication error'}))

    else:
        return redirect(reverse('home',kwargs={"error":'Authetication error'}))
       