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
    url(r'^explore/$', views.view_scenarios,  name="home"),
    url(r'^remove-substep/$', views.remove_state),
    url(r'^editor-substep/$', views.state_editor),
    url(r'^editor-substep-actions/$', views.get_components_list),
    url(r'^editor-substep-params/$', views.get_component_params),
    url(r'^editor-class-params/$', views.get_component_class_params),
    url(r'^editor-substep-update/$', views.update_state),
)