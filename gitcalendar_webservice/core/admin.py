from django.contrib import admin
from .models import GitLabAPI, CalendarConfiguration

admin.site.register(GitLabAPI)
admin.site.register(CalendarConfiguration)
# Register your models here.
