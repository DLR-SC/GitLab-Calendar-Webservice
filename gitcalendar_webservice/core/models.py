from django.conf import global_settings
from django.db import models
from django.contrib.auth.models import User


class GitLabAPI(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_name = models.CharField(max_length=100)
    url = models.URLField()
    gitlab_api_token = models.CharField(max_length=300)

    def __str__(self):
        return self.api_name


class CalendarConfiguration(models.Model):
    config_name = models.CharField(max_length=20)
    api = models.ForeignKey(GitLabAPI, on_delete=models.CASCADE)
    only_issues = models.BooleanField(verbose_name="Only Issues")
    only_milestones = models.BooleanField(verbose_name="Only Milestones")

    def __str__(self):
        return self.config_name
