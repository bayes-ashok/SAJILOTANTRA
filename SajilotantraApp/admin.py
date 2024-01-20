from django.contrib import admin

from .models import GovernmentProfile, Guidance, Notification, Post, ReportedPost

admin.site.register(Guidance)
admin.site.register(Notification)
admin.site.register(Post)

@admin.register(ReportedPost)
class ReportedPostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'reason')


from SajilotantraApp.models import Event

admin.site.register(GovernmentProfile)
admin.site.register(Event)

# feedback
from .models import Feedback, UploadedFile

class UploadedFileInline(admin.TabularInline):
    model = UploadedFile



