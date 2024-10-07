from typing import Any
from django.db import models
from datetime import datetime
class BloodTypes(models.TextChoices):
    AX = "A+"
    A_ = "A-"
    BX = "B+"
    B_ = "B-"
    OX = "O+"
    O_ = "O-"
    ABX = "AB+"
    AB_ = "AB-"

class Admin(models.Model):
    
    name = models.CharField(max_length=50,blank=False)
    id = models.IntegerField(primary_key=True,blank=False)
    dob = models.DateField(blank=False)
    isAdmin = models.BooleanField(default=False)
    isCampOrg = models.BooleanField(default=False)
    isHosp = models.BooleanField(default=False)
    belongs = models.CharField(max_length=120,blank=False)

    def __str__(self):
        return f"{self.name} - {self.id}"

class Donor(models.Model):
    name = models.CharField(max_length=50,blank=False)
    id = models.IntegerField(primary_key=True,blank=False)
    dob = models.DateField(blank=False)
    weight = models.IntegerField()
    height = models.IntegerField()
    addr = models.CharField(max_length=225)
    blood_type = models.CharField(max_length=3,choices=BloodTypes,blank=False)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
    
class Bank(models.Model):
    name = models.CharField(max_length=50,blank=False)
    id = models.IntegerField(primary_key=True,blank=False)
    addr = models.CharField(max_length=225,blank=False)
    loc = models.CharField(max_length=225,blank=False)
    owned = models.ForeignKey(to=Admin,on_delete=models.CASCADE)
    capacity = models.IntegerField(blank=False)
    a_plus = models.IntegerField(default=0)
    a_minus = models.IntegerField(default=0)
    b_plus = models.IntegerField(default=0)
    b_minus = models.IntegerField(default=0)
    ab_plus = models.IntegerField(default=0)
    ab_minus = models.IntegerField(default=0)
    o_plus = models.IntegerField(default=0)
    o_minus = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.loc}"
    
class Camp(models.Model):
    name = models.CharField(max_length=50,blank=False)
    id = models.IntegerField(primary_key=True,blank=False)
    addr = models.CharField(max_length=225,blank=False)
    loc = models.CharField(max_length=225,blank=False)
    owned = models.ForeignKey(to=Admin,on_delete=models.CASCADE)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    
    def __str__(self):
        return f"{self.name} - {self.id} - {self.start} => {self.end}"