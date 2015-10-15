__author__ = 'NBUCHINA'

from django.conf.urls import patterns, url
from translator import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.create, name='create'),
    url(r'^translate/$', views.translate, name='translate-engine'),
    url(r'^csv/$', views.csv, name="csv-generator"),
    url(r'^save/$', views.save_program, name="save-program"),
    url(r'^view/(?P<program_id>[0-9]+)/?$', views.edit, name="view"),
    url(r'^explore/$', views.view_scenarios, name="explore"),
    url(r'^remove-substep/$', views.remove_state,name="remove-substep"),
    url(r'^editor-substep/$', views.state_editor,name="edit-substep"),
    url(r'^editor-substep-actions/$', views.get_components_list,name="substep-actions"),
    url(r'^editor-substep-params/$', views.get_component_params,name="substep-params"),
    url(r'^editor-class-params/$', views.get_component_class_params,name="substep-class"),
    url(r'^editor-substep-update/$', views.update_state,name="update-substep"),
)