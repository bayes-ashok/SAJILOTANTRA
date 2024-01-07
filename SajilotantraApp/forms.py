from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'category', 'thumbnail']



from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class CustomUserChangeForm(UserChangeForm):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

