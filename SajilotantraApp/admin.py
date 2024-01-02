from django.contrib import admin

# from SajilotantraApp.models import User
from .models import Post

from .models import GovernmentProfile, Guidance, Notification

# Register your models here.

# admin.site.register(User)
admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import Event, User

admin.site.register(GovernmentProfile)

admin.site.register(Event)

admin.site.register(Post)


# 
# from django.contrib import admin
# from .models import GovernmentProfile, Guidance, Notification, Event, Category, Post
# from django.contrib.auth.models import User as AuthUser

# # Register your models here.
# admin.site.register(GovernmentProfile)
# admin.site.register(Guidance)
# admin.site.register(Notification)
# admin.site.register(Event)
# admin.site.register(Category)
# admin.site.register(Post)

## Register custom User model if available
## Replace 'User' with your custom user model if you have one
# admin.site.register(AuthUser)

