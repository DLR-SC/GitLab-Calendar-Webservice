from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from django.views import generic
from core.models import GitLabAPI, CalendarConfiguration
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


class GitLabAPIListView(ListView):
    model = GitLabAPI
    template_name = 'gitlab_api_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(user=user)


class AllGitLabAPIListView(ListView):
    model = GitLabAPI
    template_name = 'gitlab_api_list.html'
    queryset = GitLabAPI.objects.all()


class GitLabAPIDetailView(generic.DetailView):
    model = GitLabAPI
    template_name = 'gitlab_api_detail.html'

    def get_queryset(self):
        api = get_object_or_404(GitLabAPI, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(api_name=api.api_name)


class GitLabAPICreateView(generic.CreateView):
    model = GitLabAPI
    template_name = 'gitlab_api_creation.html'
    fields = ['user',
              'api_name',
              'url',
              'gitlab_api_token',
              ]

    def get_success_url(self):
        return reverse('core:all.gitlabapi.list')


def not_found(request, exception):
    """
    Shortcut view to render the default 404 site.
    """
    #   return render(request, '404.html')
    return HttpResponse("Not found", status=404)


def permission_denied(request, exception):
    """
    Shortcut view to render the default 403 site
    """
    #   return render(request, '403.html')

    return HttpResponse("Permission Denied", status=403)
