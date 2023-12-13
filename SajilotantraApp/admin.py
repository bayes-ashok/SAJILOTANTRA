from django.contrib import admin

from SajilotantraApp.models import User

from .models import Guidance

# Register your models here.

admin.site.register(User)
admin.site.register(Guidance)