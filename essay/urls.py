from django.urls import path

from . import views

app_name = 'essay'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('build', views.build, name='build'),
    path('span', views.span, name='span'),
    path('ideas', views.ideas, name='ideas'),
]