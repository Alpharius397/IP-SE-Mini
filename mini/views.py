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

def login_view(req,**opt):
    if req.method=='GET': 
        context = {i:j for i,j in opt.items()}
        print(context)
        return render(req,'home/login.html',context=context)
    
    if req.method=='POST':
        user,password,who = req.POST.get('user',None), req.POST.get('password',None), req.POST.get('who',None)
        if (not user) or (not password) or (who not in ['donor','admin']): return redirect(reverse('login',kwargs={'error':'Auth Error'}))
        
        userThis = models.Donor.objects.filter(id=user).values() if who=='donor' else models.Admin.objects.filter(id=user).values()
    
        if len(userThis)<1:
            return redirect(reverse('login',kwargs={'error':'User not Found'}))
        
        userThis = userThis[0]
        
        if check_password(password,userThis['passwrd']):
            req.session['user'] = userThis['name']
            return redirect(reverse('home',kwargs={'error':'User Authethicated, Welcome!'}))

        else:
            return redirect(reverse('login',kwargs={'error':'Password Do Not Match!'}))

def register_view(req,**opt):
    if req.method=='GET': 
        context = {i:j for i,j in opt.items()}
        return render(req,'home/register.html',context=context)
    
    if req.method=='POST':
        who = req.POST['who']
        if (who not in ['donor','admin']): return redirect(reverse('register',kwargs={'error':'Auth Error'}))
        
        userThis = models.Donor.objects.filter(id=user).values() if who=='donor' else models.Admin.objects.filter(id=user).values()
    
        if len(userThis)<1:
            return redirect(reverse('register',kwargs={'error':'User not Found'}))
        
        userThis = userThis[0]
        
        if check_password(password,userThis['passwrd']):
            req.session['user'] = userThis['name']
            return redirect(reverse('home',kwargs={'error':'User Authethicated, Welcome!'}))

        else:
            return redirect(reverse('register',kwargs={'error':'Password Do Not Match!'}))
        
def logout_user(req):
    req.session['user'] = None
    return redirect(reverse('home',kwargs={'error':'Logout Successully'}))