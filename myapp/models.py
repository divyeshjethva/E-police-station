from django.db import models
from django.utils import timezone

# Create your models here.

class Citizen(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20,default="citizen")
    
    def __str__(self):
        return f"{self.name} | {self.role} |   {self.email}"
    
class Complaint(models.Model):
    citizen = models.ForeignKey(Citizen,on_delete=models.CASCADE)
    
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    locations = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    remark = models.CharField(max_length=200,default="----")
    evidence = models.ImageField(default='',upload_to="evidence")
    status = models.CharField(default='pending')
    Inspector = models.CharField(default="---")
    
    def __str__(self):
        return f"{self.citizen.name} | {self.status}"
    
class MissingPerson(models.Model):
    citizen = models.ForeignKey(Citizen,on_delete=models.CASCADE)
    
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    date = models.DateField()
    photo = models.ImageField(default="",upload_to="missing")
    
class Inspector(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    area = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"