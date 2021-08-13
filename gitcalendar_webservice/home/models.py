from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.conf import global_settings


class GitLabAPI(models.Model):
    user_obj = User.get_username()
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, editable=True)
    api_name = models.CharField(max_length=100)
    url = models.URLField()
    gitlab_api_token = models.CharField(max_length=300)

    def __str__(self):
        return self.api_name

    def __unicode__(self):
        return self.user.id


class CalendarConfiguration(models.Model):
    config_name = models.CharField(max_length=20)
    api = models.ForeignKey(GitLabAPI, on_delete=models.CASCADE)
    only_issues = models.BooleanField(verbose_name="Only Issues")
    only_milestones = models.BooleanField(verbose_name="Only Milestones")

    def __str__(self):
        return self.config_name
