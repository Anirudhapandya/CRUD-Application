from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Company_name =models.CharField(max_length=200)
    Email_name =models.CharField(max_length=200) 
    Phone_number =models.CharField(max_length=10)
    Subject_name =models.CharField(max_length=100)
    Password =models.CharField(max_length=500,blank=True,null=True)
    address = models.TextField()
    is_active=models.BooleanField(default=True)