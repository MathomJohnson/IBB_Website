from django.contrib import admin
from .models import GoogleToken, Meeting, ScheduledMeeting

# Register your models here.
admin.site.register(GoogleToken)
admin.site.register(Meeting)
admin.site.register(ScheduledMeeting)
