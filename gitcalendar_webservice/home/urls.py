from django.urls import path
from django.views.generic.base import TemplateView

from home import views

app_name = 'home'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='homesite'),
]
