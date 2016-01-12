from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'English2NAO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^translator/', include('translator.urls', namespace="translator")),
    url(r"^account/", include("account.urls")),
    url(r'^home/', TemplateView.as_view(template_name="translator/profile.html"), name="home"),
    url(r'^$', TemplateView.as_view(template_name="translator/profile.html"), name="home")
)
