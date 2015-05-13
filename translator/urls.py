__author__ = 'NBUCHINA'

from django.conf.urls import patterns, url
from translator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.create, name='create'),
    url(r'^translate/$', views.translate),
    url(r'^csv/$', views.csv),
    url(r'^save/$', views.save_program),
    url(r'^view/(?P<program_id>[0-9]+)/?$', views.edit),
    url(r'^explore/$', views.view_scenarios),
    url(r'^remove-substep/$', views.remove_substep),
    url(r'^editor-substep/$', views.substep_editor),
    url(r'^editor-substep-actions/$', views.substep_editor_components_list),
    url(r'^editor-substep-actions/$', views.substep_editor_components_list),
    url(r'^editor-substep-params/$', views.substep_editor_params),
)