from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=200)
    lName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    

    def __str__(self):
        return self.user_id

class GovernmentProfile(models.Model):
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    description = models.TextField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name