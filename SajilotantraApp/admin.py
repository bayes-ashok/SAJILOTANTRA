from django.contrib import admin

from SajilotantraApp.models import User
<<<<<<< HEAD
from .models import GovernmentProfile
# Register your models here.

admin.site.register(User)
admin.site.register(GovernmentProfile)
=======

from .models import Guidance, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import User,Event

admin.site.register(Event)
>>>>>>> 3156e6becd7ddac663e3db536d4a40afe21ea2d9
