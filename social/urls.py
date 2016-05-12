from django.conf.urls import patterns, url
from social import views

__author__ = 'NBUCHINA'

urlpatterns = patterns('',
                       url(r'^$', views.main_page,name="home")
)