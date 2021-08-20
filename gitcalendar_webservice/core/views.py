from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from core.models import GitLabAPI, CalendarConfiguration
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm


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


def index(request):
    username = request.user.username
    api_name = request.POST.get("api_nameInput")
    url = request.POST.get("urlInput")
    gitlab_api_token = request.POST.get("gitlab_api_tokenInput")
    if api_name is None:
        username = ""
        api_name = ""
        url = ""
        gitlab_api_token = ""
    context = {
        'user': username,
        'api_name': api_name,
        'url': url,
        'gitlab_api_token': gitlab_api_token,
    }
    try:
        user_from_database = User.objects.get(username=username)
        api = GitLabAPI(user=user_from_database, api_name=api_name, url=url, gitlab_api_token=gitlab_api_token)
        api.save()
        response = redirect("core:user.gitlabapi.list", user_from_database.id)
        return response
    except:
        return render(request, 'gitlab_api_creation.html', context)


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('core:homesite')
    return render(request, 'registration/signup.html', {'form': form})
