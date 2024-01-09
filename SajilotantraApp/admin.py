from django.contrib import admin

from .models import GovernmentProfile, Guidance, Notification

admin.site.register(Guidance)
admin.site.register(Notification)
from SajilotantraApp.models import Event

admin.site.register(GovernmentProfile)
admin.site.register(Event)

# feedback
from .models import Feedback, UploadedFile

class UploadedFileInline(admin.TabularInline):
    model = UploadedFile

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    inlines = [UploadedFileInline]

admin.site.register(UploadedFile)
