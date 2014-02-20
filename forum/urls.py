from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'message/(?P<id>\d+)/', views.message, name='message'),
    url(r'$', views.index, name='index'),
)