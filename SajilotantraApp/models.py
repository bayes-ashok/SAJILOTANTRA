from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     fName = models.CharField(max_length=200)
#     lName = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
    # image = models.ImageField()

    # def __str__(self):
    #     return self.user_id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images/', null=True, blank=True)
    cover = models.ImageField(upload_to='static/cover_images/', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    # Add other fields as needed

    def str(self):
        return self.user.username

class GovernmentProfile(models.Model):
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    description = models.TextField()
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
    

# class Post(models.Model):
#     CATEGORY_CHOICES = [
#         ('query', 'Query'),
#         ('rant', 'Rant'),
#         ('problem', 'Problem'),
#         ('local_government', 'Local Government'),
#     ]

#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming Django's built-in User model
#     caption = models.TextField()
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_no w_add=True)

#     def __str__(self):
#         return self.caption[:50]
    
from django.contrib.auth.models import User
from django.db import models

CATEGORY_CHOICES = (
    ('query', 'Query'),
    ('rant', 'Rant'),
    ('problems', 'Problems'),
    ('local government', 'Local Government')
)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.caption[:50]
    
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def update_password(self, new_password):
        self.password = new_password
        print(f"Password updated for user '{self.username}'.")

# Example usage:
# Create a user instance
user1 = User("example_user", "old_password")

# Update password
new_password = "new_secure_password"
user1.update_password(new_password)
 
