from django.urls import path

from . import views

app_name = 'essay'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('build', views.build, name='build'),
    path('questions', views.questions, name='questions'),
    path('draft', views.draft, name='draft'),
    path('read', views.read, name='read'),
    path('parse', views.parse, name='parse'),
    path('ideas', views.ideas, name='ideas'),
]