# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
#from django.core.paginator import Paginator

# Create your models here.
class QuestionManager(models.Manager):
  def new(self):
#    return self.order_by('-added_at')
    return self.order_by('-id')
  def popular(self):
    return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=128) #- заголовок вопроса
    text = models.TextField() #- полный текст вопроса
    added_at = models.DateField(auto_now_add=True) #- дата добавления вопроса
    rating = models.IntegerField(default=0) #- рейтинг вопроса (число)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)#- автор вопроса
    likes = models.ManyToManyField(User, related_name='question_like_user') #- список пользователей, поставивших "лайк"
    
    def save_data(self, form, aut_id):
        self.title = form.cleaned_data['title']
        self.text = form.cleaned_data['title']
        self.author_id = aut_id
        self.save()
        return self.id


class Answer(models.Model): # ответ
    text = models.TextField() #- текст ответа
    added_at = models.DateField(auto_now_add=True) #- дата добавления ответа
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)#- вопрос, к которому относится ответ
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)#- автор ответа
    
    def save_data(self, form, aut, que_id):
        self.text = form.cleaned_data['text']
        self.author_id = aut
        self.question_id = que_id
        self.save()
        return self.id
