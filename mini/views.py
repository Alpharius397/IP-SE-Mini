import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import csrf_token
import json
from . import models


def home_view(req):
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    available_camp = list(models.Camp.objects.filter(end__gt=curr_date).values())
    
    for i in range(len(available_camp)):
        available_camp[i]['owned_id'] = models.Admin.objects.filter(id=available_camp[i]['owned_id']).values()[0]['belongs']
        
    return render(req,'home/index.html',context={'camps':available_camp})
        
