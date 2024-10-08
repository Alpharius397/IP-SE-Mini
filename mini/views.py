import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import csrf_token
import json
from . import models
    
def extract_data(val):
    
    res = [False]*3
    
    if val=='Admin': res[0] = True
    elif val=='CampOrg': res[1] = True
    elif val=='Hosp': res[2] = True
    
    return res

def home_view(req,**opt):
    curr_date = datetime.date.today()

    available_camp = models.Camp.objects.filter(end__gt=curr_date)
    
    context = {'camps':available_camp}
    context.update(opt)
    
    return render(req,'home/index.html',context=context)

def login_view(req,**opt):
    if req.method=='GET': 
        context = {i:j for i,j in opt.items()}
        return render(req,'home/login.html',context=context)
    
    if req.method=='POST':
        user,password,who = req.POST.get('user',None), req.POST.get('password',None), req.POST.get('who',None)
        if (not user) or (not password) or (who not in ['donor','admin']): return redirect(reverse('login',kwargs={'error':'Auth Error'}))
        
        userThis = models.Donor.objects.filter(id=user).values() if who=='donor' else models.Admin.objects.filter(id=user).values()
    
        if len(userThis)<1:
            return redirect(reverse('login',kwargs={'error':'User not Found'}))
        
        userThis = userThis[0]
        
        if check_password(password,userThis['passwrd']):
            req.session['name'] = userThis['name']
            req.session['user'] = userThis['id']
            req.session['who'] = who
            return redirect(reverse('home',kwargs={'error':'User Authethicated, Welcome!'}))

        else:
            return redirect(reverse('login',kwargs={'error':'Incorrect Password!'}))

def register_view(req,**opt):
    if req.method=='GET': 
        context = {i:j for i,j in opt.items()}
        return render(req,'home/register.html',context=context)
    
    if req.method=='POST':
        who = req.POST['who']
        if (who not in ['donor','admin']): return redirect(reverse('register',kwargs={'error':'Auth Error'}))
        
        name,id,passwrd,dob = req.POST['name'],req.POST['user'], make_password(req.POST['password']), req.POST['dob']
        exists=False
        
        if who=='donor':
            height,weight = req.POST['height'],req.POST['weight']
            addr, blood = req.POST['addr'],req.POST['blood']
            
            if len(models.Donor.objects.filter(id=id).values())>0: exists=True
            x = models.Donor(name,id,passwrd,dob,weight,height,addr,blood)
        
        elif who=='admin':
            isAdmin,isCampOrg,isHosp = extract_data(req.POST['where'])
            belongs = req.POST['belongs']
            
            if len(models.Donor.objects.filter(id=id).values())>0: exists=True
            
            x = models.Admin(name,id,passwrd,dob,isAdmin,isCampOrg,isHosp,belongs)
            
        try:
            
            if not exists: x.save()
            else: return redirect(reverse('register',kwargs={'error':'User ID Exists!'}))
            
            
            return redirect(reverse('register',kwargs={'error':'Registration Successful!'}))
        except Exception as e:
            print(e)
            return redirect(reverse('register',kwargs={'error':'Registration Failed'}))
            
        
        
def logout_user(req):
    req.session['user'] = None
    req.session['who'] = None
    req.session['name'] = None
    return redirect(reverse('home',kwargs={'error':'Logout Successful'}))

def get_status(start,end):
    
    curr = datetime.date.today()
    
    if curr<start: return 'Upcoming'
    elif curr<end: return 'Ongoing'
    else: return "Closed"
    
def camp_view(req,id=-1):
    if req.method=="GET":
        search = models.Camp.objects.filter(id=id)
        
        if len(search)<1:
            return redirect(reverse('home',kwargs={'error':'Camp ID Not Found!'}))

        color = {'Ongoing':'green','Upcoming':'grey','Closed':'red'}
        search = search[0]
        
        search.status = get_status(search.start,search.end)
        search.color = color[search.status]
        
        return render(req,'home/camp.html',context={'camp':search})

def reg_camp_view(req,**opt):
    context = {i:j for i,j in opt.items()}
    
    return render(req,'home/campreg.html',context=context)

def regCamp(req,id):
    if req.method=='GET':
        
        curr_user,curr_power = req.session.get('user',None), req.session.get('who',None)
        
        if curr_user is None: return reg_camp_view(req,error='You need to Login!')
        if curr_power not in ['admin','donor']: 
            logout_user(req)
            
            return redirect(reverse('home',kwargs={'error':'Unauthorized Entry'}))
        
        if curr_power=='admin': return reg_camp_view(req,error='You need to be a Donor!')
        
        user = models.Donor.objects.filter(id=curr_user)
        camp = {}
        if user:
            user = user[0]
            camps = models.CampReg.objects.filter(donor=user)
        
        return reg_camp_view(req,camps=camps)
            
        