from django.contrib import admin

# from SajilotantraApp.models import User

from django.contrib.auth.models import User


from .models import GovernmentProfile, Guidance, Notification

# Register your models here.

# admin.site.register(User)
admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import Event, Post

admin.site.register(GovernmentProfile)

admin.site.register(Event)
# admin(Post)

