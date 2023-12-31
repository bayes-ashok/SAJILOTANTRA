from django.contrib import admin

from .models import GovernmentProfile, Guidance, Notification

admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import Event, User

admin.site.register(GovernmentProfile)
admin.site.register(Event)