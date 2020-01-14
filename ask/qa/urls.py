from django.conf.urls import url
from qa import views

urlpatterns = [
    url(r'^(\d+)/', views.test, name='test'),
    url(r'', views.test, name='test1'),
]