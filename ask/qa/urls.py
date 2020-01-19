from django.conf.urls import url
from qa import views

urlpatterns = [
    url(r'^(\d+)/', views.question_details, name='test'),
    url(r'^$', views.question_new, name='new'), 
]