from ckeditor.fields import RichTextField
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=200)
    lName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # image = models.ImageField()

    def __str__(self):
        return self.user_id


class GovernmentProfile(models.Model):
    profile_id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    description = RichTextField() 
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Guidance(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = RichTextField() 
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    notice_id=models.AutoField(primary_key=True)
    notice_title=models.CharField(max_length=500)
    notice_description=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)
    posted_by=models.CharField(max_length=200)

    def __str__(self):
        return self.notice_title

    
class Event(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField()
    start=models.DateTimeField(null=True,blank=True)
    end=models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.name
