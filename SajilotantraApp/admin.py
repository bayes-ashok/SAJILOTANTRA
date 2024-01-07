from django.contrib import admin

# from SajilotantraApp.models import User

from .models import GovernmentProfile, Guidance, Notification

# Register your models here.

# admin.site.register(User)
admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import Event, User

admin.site.register(GovernmentProfile)

admin.site.register(Event)

from .models import Post
admin.site.register(Post)

from django.contrib.auth.models import User

# Unregister the default UserAdmin
# admin.site.unregister(User)



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

# Inside yourapp/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password', 'new_password')}),  # Add 'new_password' field
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin)  # Register UserAdmin with customizations

