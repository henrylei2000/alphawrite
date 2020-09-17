from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Transition, Verb, Thesis, Assignment, Idea, Draft, Article


def index(request):
    return render(request, 'essay/topic.html')


def dashboard(request):
    topic = request.POST['topic']
    idea = Idea(topic)

    if idea.blocked():
        return render(request, 'essay/index.html', {'idea': idea})
    else:
        return render(request, 'essay/dashboard.html', {
            'idea': idea,
            'evidence_types': ['cloud', 'cloud-rain', 'cloud-sun'],
        })


def questions(request):
    topic = request.POST['topic']
    stasis = request.POST['stasis']
    idea = Idea(topic)

    if idea.blocked():
        return
    else:
        return JsonResponse(idea.generate_question(stasis))


def ideas(request):
    topic = request.POST['topic']
    idea = Idea(topic)

    if idea.blocked():
        return render(request, 'essay/topic.html', {'idea': idea})
    else:
        return render(request, 'essay/ideas.html', {
            'idea': idea,
            'questions': idea.generate_questions,
            'evidence_types': ['cloud', 'cloud-rain', 'cloud-sun'],
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

    return JsonResponse(thesis.prepare())


def draft(request):
    elements = {
        'argument': request.POST['argument'],
        'claims': request.POST.getlist('claims[]'),
        'evidences': request.POST.getlist('evidences[]'),
        'entities': request.POST['entities'],
    }

    o = Draft(elements)
    return JsonResponse(o.generate())


def read(request):
    return render(request, 'essay/read.html')


def parse(request):
    article = Article(request.POST['content'])
    article.process()
    return render(request, 'essay/parse.html', {
        'parsed': article.parse(),
        'wc': article.words(),
        'keywords': article.keywords,

    })