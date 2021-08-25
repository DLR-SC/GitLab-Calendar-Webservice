from django.conf import global_settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class GitLabAPI(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_name = models.CharField(max_length=100)
    url = models.URLField()
    gitlab_api_token = models.CharField(max_length=100)

    def __str__(self):
        return self.api_name


class CalendarConfiguration(models.Model):
    api = models.ForeignKey(GitLabAPI, on_delete=models.CASCADE)
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    projects = models.CharField(verbose_name="Project list", max_length=100, default='')
    groups = models.CharField(verbose_name="Group list", max_length=100, default='')
    config_name = models.CharField(max_length=100)
    only_issues = models.BooleanField(verbose_name="Only issues", default=False)
    only_milestones = models.BooleanField(verbose_name="Only milestones", default=False)
    combined = models.BooleanField(verbose_name="Combined calendar", default=False)
    reminder = models.FloatField(verbose_name="Reminder", default=0)

    def __str__(self):
        return self.config_name
