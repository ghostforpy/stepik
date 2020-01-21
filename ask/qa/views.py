# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, Http404, HttpResponseRedirect
from qa.models import Question, Answer
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from qa.forms import AskForm, AnswerForm

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
            'url' : url_answer,
	    'user' : request.user,
        })
    if request.method == 'POST' and request.user.is_authenticated():
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = Answer()
            ans.save_data(form, request.user.id, id)
            return HttpResponseRedirect(reverse(question_details, args=(id,)))
        else:
            return HttpResponse('OK')
    else:
	return HttpResponseRedirect(reverse(qa_login, ))

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
	'user' : request.user,
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
	'user' : request.user,
    })


def ask(request, *args, **kwargs):
    if request.method == 'GET':
        form = AskForm()
        url_ask=reverse(ask)
        return render(request, 'qa/ask_question.html', {
    		'form' : form,
    		'url' : url_ask,
		'user' : request.user,
    		})

    if request.method == 'POST' and request.user.is_authenticated():
        form = AskForm(request.POST)
        if form.is_valid():
            que = Question()
            save_id = que.save_data(form, request.user.id)
            return HttpResponseRedirect(reverse(question_details, args=(save_id,)))
    else:
	return HttpResponseRedirect(reverse(qa_login, ))

def signup(request, *args, **kwargs):
    if request.method == 'GET':
	form = UserCreationForm()
	return render(request, 'qa/signup.html', {
        'form' : form,
        })
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
	    user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
	    user.save()
	    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
	    login(request, user)
            return HttpResponseRedirect(reverse(question_new,))
	else:
	    return HttpResponse('Not ok')


def qa_login(request, *args, **kwargs):
    if request.method == 'GET':
	form = AuthenticationForm()
	response=render(request, 'qa/login.html', {
        'form' : form,
        })
	if request.META['HTTP_REFERER'][-6:] != 'login/':
	    response.set_cookie('url_ref', request.META['HTTP_REFERER'])
	return response

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
	ref=request.COOKIES['url_ref'] if 'url_ref' in request.COOKIES else None
	if form.is_valid():
	    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
	    if user is not None:
		login(request, user)
        	return HttpResponseRedirect(ref if ref else reverse(question_new,))
	return render(request, 'qa/login.html', {
    		'form' : form,
		'errors' : 'Login/password is not correct. Try again.',
    		})
	
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])








