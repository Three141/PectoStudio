from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'settings/$', views.settings, name='settings'),
    url(r'auth/$', views.nfc_login),
    url(r'ajax/all_files\.json$', views.get_all_files),
    url(r'ajax/file/(?P<file_name>[^/]+)\.json$', views.get_file_data_by_name),
    url(r'ajax/file/(?P<file_owner>[^/]+)/(?P<file_name>\w+)\.json$', views.get_shared_file_data_by_name),
    url(r'ajax/save/(?P<file_name>[^/]+)/$', views.save_file_by_name),
    url(r'ajax/share/(?P<file_name>[^/]+)/$', views.share_file_by_name),
    url(r'ajax/new/(?P<file_name>[^/]+)/$', views.new_file),
    url(r'ajax/delete/(?P<file_name>[^/]+)/$', views.delete_file),
)