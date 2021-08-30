from django.contrib import admin
from core.models import GitLabAPI, CalendarConfiguration


class CalendarConfigurationInLine(admin.TabularInline):
    model = CalendarConfiguration
    extra = 1


class GitLabAPIAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['api_name', 'user', 'url']}),
        ('Token', {
            'classes': ['collapse'],
            'fields': ['gitlab_api_token']
        })
    ]
    inlines = [CalendarConfigurationInLine]
    list_display = ('api_name', 'user')
    list_filter = ['user_id']
    search_fields = ['api_name']


class CalendarConfigurationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['config_name', 'api', 'user', 'projects', 'groups']}),
        ('Further information', {
            'classes': ['collapse'],
            'fields': ['only_issues', 'only_milestones', 'combined']
        })
    ]
    list_display = ('config_name', 'api', 'user')
    list_filter = ['user_id']
    search_fields = ['config_name']


admin.site.register(GitLabAPI, GitLabAPIAdmin)
admin.site.register(CalendarConfiguration, CalendarConfigurationAdmin)
