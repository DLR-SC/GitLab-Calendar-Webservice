from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from core import views
from core.views import GitLabAPIListView, AllGitLabAPIListView, GitLabAPIDetailView

app_name = 'core'

handler404 = 'core.views.not_found'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='homesite'),
    path('signup/', views.signup_view, name='signup'),
    path('<int:pk>/gitlabapi/', GitLabAPIListView.as_view(), name='user.gitlabapi.list'),
    path('gitlabapi/', AllGitLabAPIListView.as_view(), name='all.gitlabapi.list'),
    path('gitlabapi/<int:pk>/', login_required(GitLabAPIDetailView.as_view()), name='gitlabapi.detail'),
    # path('gitlabapi/<int:pk>/edit', login_required(GitLabAPIDetailEditView.as_view()), name='gitlabapi.detail.edit'),
    path('gitlabapi/add/', login_required(views.index), name='gitlabapi.add'),
]
