import gitlab
from django.conf import settings
from gitcalendar.gitcalendar import converter
from django.http import HttpResponse
from core.models import CalendarConfiguration


def generator(configuration=None):

    api_url = configuration.api.url
    gitlab_api_token = configuration.api.gitlab_api_token
    api = gitlab.Gitlab(api_url, private_token=gitlab_api_token)
    api.auth()
    name = configuration.config_name + '.ics'
    path = settings.MEDIA_ROOT + "/" + str(configuration.read_token) + "/"
    converter(api, only_issues=configuration.only_issues, only_milestones=configuration.only_milestones,
              reminder=configuration.reminder,
              project_ids=configuration.get_project_ids(), group_ids=configuration.get_group_ids(),
              combined_calendar=name, target_directory_path=path)
