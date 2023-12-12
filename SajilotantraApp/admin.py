from django.contrib import admin
from SajilotantraApp.models import User
from .models import GovernmentProfile
# Register your models here.

admin.site.register(User)
admin.site.register(GovernmentProfile)