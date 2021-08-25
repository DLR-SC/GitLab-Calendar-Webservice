from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from core import views
from core.views import GitLabAPIListView, AllGitLabAPIListView, GitLabAPIDetailView, GitLabAPIUpdateView, \
    GitLabAPICreateView, GitLabAPIDeleteView, CalendarConfigurationListView, AllCalendarConfigurationListView, \
    CalendarConfigurationDetailView, CalendarConfigurationUpdateView, CalendarConfigurationDeleteView, \
    CalendarConfigurationCreateView

app_name = 'core'

handler404 = 'core.views.not_found'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='homesite'),
    path('signup/', views.signup_view, name='signup'),
    path('<int:pk>/gitlabapi/', GitLabAPIListView.as_view(), name='user.gitlabapi.list'),
    path('gitlabapi/', AllGitLabAPIListView.as_view(), name='all.gitlabapi.list'),
    path('gitlabapi/<int:pk>/', login_required(GitLabAPIDetailView.as_view()), name='gitlabapi.detail'),
    path('gitlabapi/<int:pk>/edit', login_required(GitLabAPIUpdateView.as_view()), name='gitlabapi.update'),
    path('gitlabapi/<int:pk>/delete', login_required(GitLabAPIDeleteView.as_view()), name='gitlabapi.delete'),
    path('gitlabapi/add/', login_required(GitLabAPICreateView.as_view()), name='gitlabapi.add'),
    path('<int:pk>/calendar/', CalendarConfigurationListView.as_view(), name='user.calendar.list'),
    path('calendar/', AllCalendarConfigurationListView.as_view(), name='all.calendar.list'),
    path('calendar/<int:pk>/', login_required(CalendarConfigurationDetailView.as_view()), name='calendar.detail'),
    path('calendar/<int:pk>/edit', login_required(CalendarConfigurationUpdateView.as_view()), name='calendar.update'),
    path('calendar/<int:pk>/delete', login_required(CalendarConfigurationDeleteView.as_view()), name='calendar.delete'),
    path('calendar/add/', login_required(CalendarConfigurationCreateView.as_view()), name='calendar.add'),
]
