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

    if idea.is_test():
        return render(request, 'essay/index.html', {'idea': idea})
    else:
        return render(request, 'essay/dashboard.html', {
            'topic': idea.process().topic,
            'idea': idea
        })


def build(request):
    ideas = {
        'fact1': request.POST['fact1'],
        'fact2': request.POST['fact2'],
        'definition1': request.POST['definition1'],
        'definition2': request.POST['definition2'],
        'quality1': request.POST['quality1'],
        'quality2': request.POST['quality2'],
        'policy1': request.POST['policy1'],
        'policy2': request.POST['policy2'],
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
