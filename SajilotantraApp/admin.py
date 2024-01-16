from django.contrib import admin

from .models import GovernmentProfile, Guidance, Notification, ReportedPost

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


from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import ReportedPost

@admin.register(ReportedPost)
class ReportedPostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'post')
    search_fields = ('post_id',)