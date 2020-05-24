from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Transition, Verb, Thesis, Assignment, Idea


def index(request):
    return render(request, 'essay/index.html')


def dashboard(request):
    topic = request.POST['topic']
    return render(request, 'essay/dashboard.html', {
        'topic': topic
    })


def build(request):
    components = {
        "topic": request.POST['topic'],  # name in the web form
        "opinion": request.POST['opinion'],  # name in the web form
        "argument_1": request.POST['argument_1'],  # name in the web form
        "argument_2": request.POST['argument_2'],  # name in the web form
        "counterargument": request.POST['counterargument'],  # name in the web form
        "title": request.POST['title'],  # name in the web form
    }

    phrase = Transition("sequence").get_phrase()

    verb = Verb("literary").get_verb()

    return render(request, 'essay/thesis.html', {
        'thesis': Thesis(components),  # pass the variable to html page
        'phrase': phrase,
        'verb': verb
    })


def span(request):
    assignment = request.POST['assignment']
    purpose = Assignment(assignment).process().get_purpose()
    return HttpResponse("The purpose of this writing: " + purpose)


def ideas(request):
    topic = request.POST['topic']
    nature = request.POST['nature']
    idea = Idea(topic, nature)
    return render(request, 'essay/ideas.html', {
        'topic': topic,  # pass the variable to html page
        'nature': nature,
        'questions': idea.get_questions()
    })
