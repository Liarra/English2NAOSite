from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.template import Context, RequestContext
from django.template.loader import get_template

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'English2NAO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^translator/', include('translator.urls', namespace="translator")),
    url(r"^account/", include("account.urls")),
    url(r'^$', include("social.urls"))
)
