# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.http import HttpResponse, Http404
from qa.models import Question, Answer
from django.core.paginator import Paginator

@require_GET
def question_details(request, id):
    question = get_object_or_404(Question, id=id)
    try:
	answers = Answer.objects.filter(question_id__exact=id)
#	answers = Answer.objects.get(question_id=id)
    except Answer.DoesNotExist:
	answers = None
    return render(request, 'qa/question_details.html', {
	'question' : question,
	'answers' : answers,
    })

@require_GET
def popular(request, *args, **kwargs):
    
    
    page = request.GET.get('page', 1)
    pop = Question.objects.popular()
    limit = 10
    paginator = Paginator(pop, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'qa/question_popular.html', {
	'questions' : page.object_list,
	'paginator' : paginator,
	'page' : page,
    })
    #return HttpResponse('OKpopular')

@require_GET
def question_new(request, *args, **kwargs):
    page = request.GET.get('page', 1)
    new = Question.objects.new()
    limit = 10
    paginator = Paginator(new, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'qa/question_new.html', {
	'questions' : page.object_list,
	'paginator' : paginator,
	'page' : page,
    })
    #return HttpResponse('OKnew')

# Create your views here.
