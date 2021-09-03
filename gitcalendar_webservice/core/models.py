import sys
import uuid

from django.conf import global_settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class GitLabAPI(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="api_users", null=False)
    api_name = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    gitlab_api_token = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.api_name

    def get_related(self):
        return self.configurations.all()


class CalendarConfiguration(models.Model):
    api = models.ForeignKey(GitLabAPI, on_delete=models.CASCADE, related_name="configurations")
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cal_users")
    read_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    write_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    projects = models.CharField(verbose_name="Project list", max_length=100, default='', blank=True, null=False)
    groups = models.CharField(verbose_name="Group list", max_length=100, default='', blank=True, null=False)
    config_name = models.CharField(max_length=100)
    only_issues = models.BooleanField(verbose_name="Only issues", default=False)
    only_milestones = models.BooleanField(verbose_name="Only milestones", default=False)
    reminder = models.FloatField(verbose_name="Reminder", default=0.0)
    file_exists = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.config_name

    @staticmethod
    def get_related():
        return None

    def clean(self):
        if self.projects == '' and self.groups == '':
            raise ValidationError({'projects': "Please provide an entry for at least one project/group",
                                   'groups': "Please provide an entry for at least one project/group"})

    @staticmethod
    def _convert_ids(id_string):
        """
        Converts a string of given ids into a set of integer ids
        """
        ids = set()
        if id_string != "":
            for pid in id_string.split(','):
                try:
                    ids.add(int(pid))
                except ValueError:
                    print(f"{pid} is not a valid id.", file=sys.stderr)
            return ids
        else:
            return None

    def get_project_ids(self):
        return self._convert_ids(self.projects)

    def get_group_ids(self):
        return self._convert_ids(self.groups)
