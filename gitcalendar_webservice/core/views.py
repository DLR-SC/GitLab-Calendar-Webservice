from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
from core.models import GitLabAPI, CalendarConfiguration
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin


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


class GitLabAPIListView(UserPassesTestMixin, ListView):
    model = GitLabAPI
    template_name = 'gitlabapi_list.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk'] or self.request.user.is_superuser

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(user=user)


class GitLabAPIDetailView(UserPassesTestMixin, generic.DetailView):
    model = GitLabAPI
    template_name = 'gitlabapi_detail.html'

    def test_func(self):
        return self.request.user == GitLabAPI.objects.get(pk=self.kwargs['pk']).user or \
             self.request.user.is_superuser

    def get_queryset(self):
        api = get_object_or_404(GitLabAPI, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(api_name=api.api_name)


class GitLabAPIUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = GitLabAPI
    template_name = 'gitlabapi_form.html'
    fields = [
        'api_name', 'url', 'gitlab_api_token'
    ]

    def test_func(self):
        return self.request.user == GitLabAPI.objects.get(pk=self.kwargs['pk']).user or \
             self.request.user.is_superuser

    def get_success_url(self):
        return reverse('core:user.gitlabapi.list', args=[self.object.user.pk])


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
        return self.request.user == CalendarConfiguration.objects.get(pk=self.kwargs['pk']) \
               or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('core:user.gitlabapi.list', args=[self.object.user.pk])


class CalendarConfigurationListView(UserPassesTestMixin, ListView):
    model = CalendarConfiguration
    template_name = 'calendar_list.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk'] or self.request.user.is_superuser

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return CalendarConfiguration.objects.filter(user=user)


class CalendarConfigurationDetailView(UserPassesTestMixin, generic.DetailView):
    model = CalendarConfiguration
    template_name = 'calendar_detail.html'

    def test_func(self):
        return self.request.user == CalendarConfiguration.objects.get(pk=self.kwargs['pk']).user \
               or self.request.user.is_superuser

    def get_queryset(self):
        cal = get_object_or_404(CalendarConfiguration, pk=self.kwargs['pk'])
        return CalendarConfiguration.objects.filter(config_name=cal.config_name)


class CalendarConfigurationUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = CalendarConfiguration
    template_name = 'calendar_form.html'
    fields = [
        'config_name', 'api', 'projects', 'groups', 'only_issues', 'only_milestones', 'combined',
    ]

    def test_func(self):
        return self.request.user == CalendarConfiguration.objects.get(pk=self.kwargs['pk']).user \
               or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['api'].queryset = GitLabAPI.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('core:user.calendar.list', args=[self.object.user.pk])


class CalendarConfigurationCreateView(generic.CreateView):
    model = CalendarConfiguration
    template_name = 'calendar_form.html'
    fields = [
        'config_name', 'api', 'projects', 'groups', 'only_issues', 'only_milestones', 'combined',
    ]

    # gets the apis which belong to the user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['api'].queryset = GitLabAPI.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:calendar.detail', args=[self.object.pk])


class CalendarConfigurationDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = CalendarConfiguration
    template_name = 'delete.html'

    def test_func(self):
        return self.request.user == CalendarConfiguration.objects.get(pk=self.kwargs['pk']) \
               or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('core:user.calendar.list', args=[self.object.user.pk])


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
