from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
import json
from .utils import *
# from views import huffman_decode

from Sajilotantra import settings

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     fName = models.CharField(max_length=200)
#     lName = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     image = models.ImageField(upload_to='static/profiles/', null=True, blank=True)
#     bio = models.CharField(max_length=255, null=True, blank=True)
#     # image = models.ImageField()

#     def __str__(self):
#         return self.user_id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images/', null=True, blank=True)
    cover = models.ImageField(upload_to='static/cover_images/', null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username

class GovernmentProfile(models.Model):
    profile_id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    description = RichTextField() 
    address = models.CharField(max_length=200)

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
    start=models.DateField(null=True,blank=True)
    end=models.DateField(null=True,blank=True)
    Location=models.CharField(max_length=255,null=True,blank=True)

    
    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    category = models.CharField(max_length=100)
    suggestion = models.TextField()

class UploadedFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    file = models.FileField(upload_to='static/feedback_files/')

    def __str__(self):
        return self.file.name

class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    encoded_caption = models.TextField()
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)  # New field for storing like count
    encoding_dict = models.TextField(null=True)

    def decode_caption(self):
        print(f"Encoding Dict: {self.encoding_dict}")
        if self.encoding_dict:
            encoding_dict = json.loads(self.encoding_dict)
            print(f"Decoding with Dict: {encoding_dict}")
            return huffman_decode(self.encoded_caption, encoding_dict)
        else:
            print("Unable to decode caption: Encoding Dict is None")
            return "Unable to decode caption"

    def save(self, *args, **kwargs):
        # Ensure that encoding_dict is not saved as None to prevent future errors
        if self.encoding_dict is None:
            self.encoding_dict = json.dumps({})  # Provide an empty dictionary as a default
        super().save(*args, **kwargs)

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Override save method to update like count in the associated post
        super(PostLike, self).save(*args, **kwargs)
        self.post.like_count = PostLike.objects.filter(post=self.post).count()
        self.post.save()

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)