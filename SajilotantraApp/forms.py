from django import forms
from .models import GovernmentProfile

class GovernmentProfileForm(forms.ModelForm):
    class Meta:
        model = GovernmentProfile
        fields = ['name', 'thumbnail', 'description', 'address']
