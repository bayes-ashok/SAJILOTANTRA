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

<<<<<<< HEAD

class GovernmentProfile(models.Model):
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    description = models.TextField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Guidance(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField() 
    thumbnail = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


=======
class Notification(models.Model):
    notice_id=models.AutoField(primary_key=True)
    notice_title=models.CharField(max_length=500)
    notice_description=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)
    posted_by=models.CharField(max_length=200)

    def __str__(self):
        return self.notice_title
>>>>>>> 5c87ca808b85ad5a9949ba1e5ff741e94265d5a4
