# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, Http404, HttpResponseRedirect
from qa.models import Question, Answer
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from qa.forms import AskForm, AnswerForm

#@require_GET
def question_details(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, id=id)
        form = AnswerForm()
        url_answer = reverse(question_details, args=(id,))
        try:
            answers = Answer.objects.filter(question_id__exact=id)
        except Answer.DoesNotExist:
            answers = None
        return render(request, 'qa/question_details.html', {
            'question' : question,
            'answers' : answers,
            'form' : form,
            'url' : url_answer
        })
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = Answer()
            ans.save_data(form, 1, id)
            return HttpResponseRedirect(reverse(question_details, args=(id,)))



@require_GET
def popular(request, *args, **kwargs):
    
    
    page = request.GET.get('page', 1)
    pop = Question.objects.popular()
    limit = 10
    paginator = Paginator(pop, limit)
    baseurl = reverse('popular')
    page = paginator.page(page)
    return render(request, 'qa/question_popular.html', {
	'questions' : page.object_list,
	'paginator' : paginator,
	'page' : page,
	'baseurl' : baseurl,
    })

@require_GET
def question_new(request, *args, **kwargs):
    page = request.GET.get('page', 1)
    new = Question.objects.new()
    limit = 10
    paginator = Paginator(new, limit)
    baseurl = reverse(question_new)
    page = paginator.page(page)
    return render(request, 'qa/question_new.html', {
	'questions' : page.object_list,
	'paginator' : paginator,
	'page' : page,
	'baseurl' : baseurl,
    })


def ask(request, *args, **kwargs):
    if request.method == 'GET':
        form = AskForm()
        url_ask=reverse(ask)
        return render(request, 'qa/ask_question.html', {
        'form' : form,
        'url' : url_ask,
        })
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            que = Question()
            save_id = que.save_data(form, 1)
            return HttpResponseRedirect(reverse(question_details, args=(save_id,)))
















