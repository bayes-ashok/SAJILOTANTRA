from django.contrib import admin

from SajilotantraApp.models import User
<<<<<<< HEAD

from .models import Guidance

# Register your models here.

admin.site.register(User)
admin.site.register(Guidance)
=======
from SajilotantraApp.models import Notification
# Register your models here.

admin.site.register(User)
admin.site.register(Notification)
>>>>>>> 5c87ca808b85ad5a9949ba1e5ff741e94265d5a4
