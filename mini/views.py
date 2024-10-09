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
            req.session['who'] = True if who=='admin' else False
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
    
def camp_view(req,id=-1,**opt):
    if req.method=="GET":
        search = models.Camp.objects.filter(id=id)
        
        if len(search)<1:
            return redirect(reverse('home',kwargs={'error':'Camp ID Not Found!'}))

        color = {'Ongoing':'green','Upcoming':'grey','Closed':'red'}
        search = search[0]
        
        search.status = get_status(search.start,search.end)
        search.color = color[search.status]
        toadd = {'already':False}
        if req.session['user'] is not None:
            try:
                curr_user = models.Donor.objects.filter(id=req.session['user'])[0] 
                toadd['already'] = True if len(models.CampReg.objects.filter(donor=curr_user,camp=search))>0 else False
            except:
                pass
        expired = True if search.status=='Closed' else False
        context = {'camp':search,'admin':req.session['who'],'expired':expired}
        context.update(opt)
        context.update(toadd)
        print(context)
        return render(req,'home/camp.html',context=context)

def reg_camp_view(req,**opt):
    
    return render(req,'home/campreg.html',context=opt)

def regCamp(req,id):
    if req.method=='GET':
        
        curr_user,curr_power = req.session.get('user',None), req.session.get('who',None)
        
        if curr_user is None: return reg_camp_view(req,error='You need to Login!')
        if curr_power not in [True,False]: 
            logout_user(req)
            
            return redirect(reverse('home',kwargs={'error':'Unauthorized Entry'}))
        
        if curr_power=='admin': return reg_camp_view(req,error='You need to be a Donor!')

        user = models.Donor.objects.filter(id=curr_user)
        camp = {}
        if user:
            user = user[0]
            camp = models.CampReg.objects.filter(donor=user)
        
        return reg_camp_view(req,camps=camp)


def reg_form(req,**opt):
    return render(req,'home/donor_reg.html',context=opt)   

def donor_reg(req,id):
    curr_user = req.session.get('user',None)
    curr_camp = models.Camp.objects.filter(id=id)
    
    if curr_user is None or len(curr_camp)<1: return redirect(reverse('home',kwargs={'error':'Must be logined in'}))
    
    user = models.Donor.objects.filter(id=curr_user)[0]
    curr_camp=curr_camp[0]
    
    return reg_form(req,camp=curr_camp,donor=user)

def confirm_reg(req,donor,camp):
    if req.method=="POST":
        donor = models.Donor.objects.filter(id=donor)
        camp = models.Camp.objects.filter(id=camp)
        
        if len(donor)<1 or len(camp)<1: return redirect(reverse('home',kwargs={'error':'User or Camp not found'}))
        
        donor = donor[0]
        camp = camp[0]
        
        # check for existing:
        z = models.CampReg.objects.filter(donor=donor,camp=camp)
        
        if z:
            return redirect(reverse('camp',kwargs={'error':"Already Registered"}))
        else:
            date = datetime.date.today()
            z=models.CampReg(donor=donor,camp=camp,date=date)
            
            try:
                z.save()
                return redirect(reverse('camp',kwargs={'id':camp.id,'error':"Registred in Camp"}))
            except:
                return redirect(reverse('camp',kwargs={'id':camp.id,'error':"Error in Registration"}))

def camps_view(req,**opt):
    return render(req,'home/camp_all.html',context=opt)

def camps_all(req,id):
    if req.method=="GET":
        admin_id = req.session.get('user',None)
        if admin_id is None: return redirect(reverse('home',kwargs={'error':'Auth error'}))
        
        camps = list(models.Camp.objects.filter(owned_id=admin_id))
        
        if not camps: return redirect(reverse('home',kwargs={'error':'No camps created'}))
        
        color = {'Ongoing':'green','Upcoming':'grey','Closed':'red'}
        
        for i in range(len(camps)):
            camps[i].count= len(models.CampReg.objects.filter(camp_id=camps[i].id).values())
            camps[i].status = get_status(camps[i].start,camps[i].end)
            camps[i].color = color[camps[i].status]
        
        return camps_view(req,camps=camps)        
        
    