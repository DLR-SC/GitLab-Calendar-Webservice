from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import RequestContext
from django.urls import reverse
from django.views import generic, View
from core.models import GitLabAPI, CalendarConfiguration
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from gitcalendar.gitcalendar import converter
from core.calendar_generator import generator
from gitlab import GitlabGetError
from django.conf import settings
import mimetypes


def is_same_user(user1, user2):
    return user1 == user2


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


def not_found(request, exception):
    """
    Shortcut view to render the default 404 site.
    """
    response = render(
        '404.html',
        RequestContext(request)
    )
    response.status_code = 404

    return response


def permission_denied(request, exception):
    """
    Shortcut view to render the default 403 site
    """
    response = render(
        '403.html',
        RequestContext(request)
    )
    response.status_code = 403

    return response


class GitLabAPIListView(ListView):
    model = GitLabAPI
    template_name = 'gitlabapi_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return GitLabAPI.objects.filter(user=user)


class GitLabAPIDetailView(UserPassesTestMixin, generic.DetailView):
    model = GitLabAPI
    template_name = 'gitlabapi_detail.html'

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)


class GitLabAPIUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = GitLabAPI
    template_name = 'gitlabapi_form.html'
    fields = [
        'api_name', 'url', 'gitlab_api_token'
    ]

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)

    def get_success_url(self):
        return reverse('core:gitlabapi.detail', args=[self.object.pk])


class GitLabAPICreateView(generic.CreateView):
    model = GitLabAPI
    template_name = 'gitlabapi_form.html'
    fields = [
        'api_name', 'url', 'gitlab_api_token'
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:gitlabapi.detail', args=[self.object.pk])


class GitLabAPIDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = GitLabAPI
    template_name = 'delete.html'

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)

    def get_success_url(self):
        return reverse('core:gitlabapi.list')


class CalendarConfigurationListView(ListView):
    model = CalendarConfiguration
    template_name = 'calendar_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return CalendarConfiguration.objects.filter(user=user)


class CalendarConfigurationDetailView(UserPassesTestMixin, generic.DetailView):
    model = CalendarConfiguration
    template_name = 'calendar_detail.html'

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)


class CalendarConfigurationUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = CalendarConfiguration
    template_name = 'calendar_form.html'
    fields = [
        'config_name', 'api', 'projects', 'groups', 'only_issues', 'only_milestones'
    ]

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['api'].queryset = form.fields['api'].queryset.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return reverse('core:calendar.detail', args=[self.object.pk])


class CalendarConfigurationCreateView(generic.CreateView):
    model = CalendarConfiguration
    template_name = 'calendar_form.html'
    fields = [
        'config_name', 'api', 'projects', 'groups', 'only_issues', 'only_milestones'
    ]

    # gets the apis which belong to the user
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['api'].queryset = form.fields['api'].queryset.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:calendar.detail', args=[self.object.pk])


class CalendarConfigurationDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = CalendarConfiguration
    template_name = 'delete.html'

    def test_func(self):
        return is_same_user(self.request.user, self.get_object().user)

    def get_success_url(self):
        return reverse('core:calendar.list')


def calendar_generating(request, token=None):

    try:
        config = CalendarConfiguration.objects.get(write_token__exact=token) # write token
        generator(config)
        config.file_exists = True
        config.save()
        return HttpResponseRedirect(reverse('core:calendar.detail', args=[config.pk]))
    except GitlabGetError as e:
        response = render(request, '400.html', {'message': 'GitLab Authentication failed'})
        response.status_code = 400
        return response


def show_file(request, token=None, filename=None):
    path = settings.MEDIA_ROOT + "/" + str(token) + "/" + filename
    with open(path, "r") as file:
        content = file.read()

    return HttpResponse(content, content_type="text/plain; encoding")
