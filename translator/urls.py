__author__ = 'NBUCHINA'

from django.conf.urls import patterns, url
from translator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.create, name='create'),
    url(r'^translate/$', views.translate)
)