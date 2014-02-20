from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'packages': ('PectoStudio',),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PectoStudio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^forum/', include('forum.urls')),
    url(r'^', include('main.urls')),
)