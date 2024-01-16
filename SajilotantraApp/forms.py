# forms.py
from django import forms
from .models import ReportedPost

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportedPost
        fields = ['post_id', 'post']
