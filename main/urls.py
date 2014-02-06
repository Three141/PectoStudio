from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^ajax/all_files\.json$', views.get_all_files),
    url(r'^ajax/file/(?P<file_name>\w+)\.json$', views.get_file_data_by_name),
    url(r'^ajax/save/(?P<file_name>\w+)/$', views.save_file_by_name),
    url(r'^ajax/new/(?P<file_name>\w+)/$', views.new_file),
    url(r'^ajax/delete/(?P<file_name>\w+)/$', views.delete_file),
)