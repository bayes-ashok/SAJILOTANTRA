import json

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from Sajilotantra import settings

from .utils import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/profile_images/', blank=True, default='static/assets/images/defaultuser.png')    
    cover = models.ImageField(upload_to='static/cover_images/', default='static/assets/images/default_cover.png', blank=True)    
    bio = models.CharField(max_length=255, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, default='')

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
    comment_count=models.IntegerField(default=0)
    encoding_dict = models.TextField(null=True)
    
    def is_liked_by_user(self, user):
        return self.postlike_set.filter(user=user).exists()   
        

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
        if self.encoding_dict is None:
            self.encoding_dict = json.dumps({})  
        super().save(*args, **kwargs)

    def delete_post(self):

        self.delete()
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(PostLike, self).save(*args, **kwargs)
        self.post.like_count = PostLike.objects.filter(post=self.post).count()
        self.post.save()

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(PostComment, self).save(*args, **kwargs)
        self.post.comment_count=PostComment.objects.filter(post=self.post).count()
        self.post.save()
        
class ReportedPost(models.Model):
    post_id = models.IntegerField()
    reason = models.TextField()
    
    def __str__(self):
        return f"Report for Post ID: {self.post_id}"    

