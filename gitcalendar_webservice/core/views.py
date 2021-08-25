from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from core.models import GitLabAPI, CalendarConfiguration
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm


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


class GitLabAPIListView(ListView):
    model = GitLabAPI
    template_name = 'gitlab_api_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(user=user)


class AllGitLabAPIListView(ListView):
    model = GitLabAPI
    template_name = 'gitlab_api_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GitLabAPI.objects.all()
        else:
            return GitLabAPI.objects.filter(user=self.request.user)


class GitLabAPIDetailView(generic.DetailView):
    model = GitLabAPI
    template_name = 'gitlab_api_detail.html'

    def get_queryset(self):
        api = get_object_or_404(GitLabAPI, pk=self.kwargs['pk'])
        return GitLabAPI.objects.filter(api_name=api.api_name)


class GitLabAPIUpdateView(generic.UpdateView):
    model = GitLabAPI
    template_name = 'gitlabapi_form.html'
    fields = [
        'api_name', 'url', 'gitlab_api_token'
    ]

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


class GitLabAPIDeleteView(generic.DeleteView):
    model = GitLabAPI
    template_name = 'delete.html'

    def get_success_url(self):
        # decide whether returning to all api page or only to the users himself
        if self.request.user == self.object.user:
            return reverse('core:user.gitlabapi.list', args=[self.object.user.pk])
        else:
            return reverse('core:all.gitlabapi.list')


class CalendarConfigurationListView(ListView):
    model = CalendarConfiguration
    template_name = 'calendar_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return CalendarConfiguration.objects.filter(user=user)


class AllCalendarConfigurationListView(ListView):
    model = CalendarConfiguration
    template_name = 'calendar_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CalendarConfiguration.objects.all()
        else:
            return CalendarConfiguration.objects.filter(user=self.request.user)


class CalendarConfigurationDetailView(generic.DetailView):
    model = CalendarConfiguration
    template_name = 'calendar_detail.html'

    def get_queryset(self):
        cal = get_object_or_404(CalendarConfiguration, pk=self.kwargs['pk'])
        return CalendarConfiguration.objects.filter(config_name=cal.config_name)


class CalendarConfigurationUpdateView(generic.UpdateView):
    model = CalendarConfiguration
    template_name = 'calendar_form.html'
    fields = [
        'config_name', 'api', 'projects', 'groups', 'only_issues', 'only_milestones', 'combined',
    ]

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
        form.api.queryset = GitLabAPI.objects.filter(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:calendar.detail', args=[self.object.pk])


class CalendarConfigurationDeleteView(generic.DeleteView):
    model = CalendarConfiguration
    template_name = 'delete.html'

    def get_success_url(self):
        # decide whether returning to all api page or only to the users himself
        if self.request.user == self.object.user:
            return reverse('core:user.calendar.list', args=[self.object.user.pk])
        else:
            return reverse('core:all.calendar.list')


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
