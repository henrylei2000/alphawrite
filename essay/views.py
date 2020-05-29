from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Transition, Verb, Thesis, Assignment, Idea


def index(request):
    return render(request, 'essay/index.html')


def dashboard(request):
    topic = request.POST['topic']
    idea = Idea(topic)

    if idea.blocked():
        return render(request, 'essay/index.html', {'idea': idea})
    else:
        return render(request, 'essay/dashboard.html', {
            'topic': idea.process().topic,
            'idea': idea
        })


def build(request):
    ideas = {
        'fact': request.POST['fact'],
        'definition': request.POST['definition'],
        'quality': request.POST['quality'],
        'counterpoint': request.POST['counterpoint'],
        'policy': request.POST['policy'],
    }
    thesis = Thesis(ideas)

    return JsonResponse(thesis.build())


def span(request):
    assignment = request.POST['assignment']
    purpose = Assignment(assignment).process().get_purpose()
    return JsonResponse({'topic': "The purpose of this writing: " + purpose})


def ideas(request):
    topic = request.POST['topic']
    nature = request.POST['nature']
    idea = Idea(topic, nature)
    return render(request, 'essay/ideas.html', {
        'topic': topic,  # pass the variable to html page
        'nature': nature,
        'questions': idea.get_questions()
    })
