from django.conf import global_settings
from django.db import models
from django.contrib.auth.models import User


class GitLabAPI(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_users")
    api_name = models.CharField(max_length=100)
    url = models.URLField()
    gitlab_api_token = models.CharField(max_length=100)

    def __str__(self):
        return self.api_name

    def get_related(self):
        return self.configurations.all()


class CalendarConfiguration(models.Model):
    api = models.ForeignKey(GitLabAPI, on_delete=models.CASCADE, related_name="configurations")
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cal_users")
    projects = models.CharField(verbose_name="Project list", max_length=100, default='', blank=True)
    groups = models.CharField(verbose_name="Group list", max_length=100, default='', blank=True)
    config_name = models.CharField(max_length=100)
    only_issues = models.BooleanField(verbose_name="Only issues", default=False)
    only_milestones = models.BooleanField(verbose_name="Only milestones", default=False)
    combined = models.BooleanField(verbose_name="Combined calendar", default=False)
    reminder = models.FloatField(verbose_name="Reminder", default=0)

    def __str__(self):
        return self.config_name

    @staticmethod
    def get_related():
        return None
